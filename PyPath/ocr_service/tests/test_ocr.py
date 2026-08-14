"""Unit tests for image preprocessing and mocked Tesseract interactions."""

from __future__ import annotations

from unittest.mock import patch

import cv2
import numpy as np
import pytest

from app.errors import InvalidImageError
from app.ocr import extract_python_code, preprocess_code_image


def _png_bytes() -> bytes:
    image = np.full((80, 260, 3), 255, dtype=np.uint8)
    cv2.putText(
        image,
        "print(42)",
        (5, 45),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.7,
        (0, 0, 0),
        2,
    )
    succeeded, encoded = cv2.imencode(".png", image)
    assert succeeded
    return encoded.tobytes()


def test_preprocess_returns_binary_image(settings) -> None:
    processed = preprocess_code_image(_png_bytes(), settings)

    assert processed.ndim == 2
    assert set(np.unique(processed)).issubset({0, 255})


def test_extract_python_code_uses_mocked_tesseract(settings) -> None:
    mock_data = {"text": ["print(42)"], "conf": ["92.5"]}
    with (
        patch(
            "app.ocr.pytesseract.image_to_string",
            return_value="print(42)\n",
        ) as text_ocr,
        patch(
            "app.ocr.pytesseract.image_to_data",
            return_value=mock_data,
        ) as data_ocr,
    ):
        result = extract_python_code(_png_bytes(), settings)

    assert result.code == "print(42)"
    assert result.confidence == 92.5
    assert text_ocr.called
    assert data_ocr.called


def test_rejects_invalid_image(settings) -> None:
    with pytest.raises(InvalidImageError, match="readable image"):
        preprocess_code_image(b"not an image", settings)
