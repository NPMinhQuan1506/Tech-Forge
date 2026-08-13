"""OpenCV preprocessing and Tesseract extraction for photographed Python code."""

from __future__ import annotations

from dataclasses import dataclass

import cv2
import numpy as np
import pytesseract

from .config import Settings
from .errors import InvalidImageError, OcrUnavailableError


@dataclass(frozen=True, slots=True)
class OcrExtraction:
    """OCR text and a best-effort mean word confidence percentage."""

    code: str
    confidence: float | None


def _decode_image(image_bytes: bytes, settings: Settings) -> np.ndarray:
    """Decode and reject invalid or excessively large images."""
    if not image_bytes:
        raise InvalidImageError("The uploaded image is empty.")

    encoded_image = np.frombuffer(image_bytes, dtype=np.uint8)
    image = cv2.imdecode(encoded_image, cv2.IMREAD_UNCHANGED)
    if image is None or image.size == 0:
        raise InvalidImageError("The uploaded file is not a readable image.")

    height, width = image.shape[:2]
    if height * width > settings.max_image_pixels:
        raise InvalidImageError(
            "The image dimensions exceed the configured pixel safety limit."
        )

    return image


def preprocess_code_image(image_bytes: bytes, settings: Settings) -> np.ndarray:
    """Improve contrast and character separation before Tesseract reads code.

    The transformations deliberately preserve line layout and spaces: Python
    indentation matters, so this function does not deskew or crop aggressively.
    """
    image = _decode_image(image_bytes, settings)

    if image.ndim == 2:
        grayscale = image
    elif image.shape[2] == 4:
        grayscale = cv2.cvtColor(image, cv2.COLOR_BGRA2GRAY)
    else:
        grayscale = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # A modest 2x upscale gives Tesseract more pixels for punctuation such as
    # colons, underscores, parentheses, and Python indentation.
    grayscale = cv2.resize(
        grayscale,
        None,
        fx=2,
        fy=2,
        interpolation=cv2.INTER_CUBIC,
    )
    contrast_enhanced = cv2.createCLAHE(
        clipLimit=2.0,
        tileGridSize=(8, 8),
    ).apply(grayscale)
    denoised = cv2.fastNlMeansDenoising(
        contrast_enhanced,
        None,
        h=10,
        templateWindowSize=7,
        searchWindowSize=21,
    )
    return cv2.adaptiveThreshold(
        denoised,
        maxValue=255,
        adaptiveMethod=cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        thresholdType=cv2.THRESH_BINARY,
        blockSize=31,
        C=11,
    )


def _mean_confidence(ocr_data: dict[str, list[object]]) -> float | None:
    """Calculate a confidence score without treating -1 layout values as words."""
    confidences: list[float] = []
    text_items = ocr_data.get("text", [])
    confidence_items = ocr_data.get("conf", [])

    for text, confidence in zip(text_items, confidence_items):
        if not str(text).strip():
            continue
        try:
            confidence_value = float(str(confidence))
        except ValueError:
            continue
        if confidence_value >= 0:
            confidences.append(confidence_value)

    if not confidences:
        return None
    return round(sum(confidences) / len(confidences), 2)


def _normalise_ocr_code(raw_code: str) -> str:
    """Make only non-semantic OCR normalisations; do not guess Python syntax."""
    return (
        raw_code.replace("\r\n", "\n")
        .replace("\r", "\n")
        .replace("\u00a0", " ")
        .strip("\n")
    )


def extract_python_code(image_bytes: bytes, settings: Settings) -> OcrExtraction:
    """Run Tesseract with a block-of-code page segmentation configuration."""
    processed_image = preprocess_code_image(image_bytes, settings)
    if settings.tesseract_cmd:
        pytesseract.pytesseract.tesseract_cmd = settings.tesseract_cmd

    config = "--oem 3 --psm 6 -c preserve_interword_spaces=1"
    try:
        raw_code = pytesseract.image_to_string(
            processed_image,
            lang=settings.ocr_language,
            config=config,
        )
        ocr_data = pytesseract.image_to_data(
            processed_image,
            lang=settings.ocr_language,
            config=config,
            output_type=pytesseract.Output.DICT,
        )
    except (pytesseract.TesseractNotFoundError, pytesseract.TesseractError) as error:
        raise OcrUnavailableError(
            "Tesseract OCR is unavailable. Check TESSERACT_CMD and installed languages."
        ) from error
    except RuntimeError as error:
        raise OcrUnavailableError(
            "Tesseract OCR could not process this image."
        ) from error

    code = _normalise_ocr_code(raw_code)
    if not code.strip():
        raise InvalidImageError("No Python code could be extracted from the image.")

    return OcrExtraction(code=code, confidence=_mean_confidence(ocr_data))
