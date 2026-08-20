"""Configuration for the OCR grading service.

The service deliberately reads plain environment variables instead of relying on
a framework-specific settings module, so it can run as an independent
microservice or in a container.
"""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv


def _bounded_int(name: str, default: int, minimum: int, maximum: int) -> int:
    """Read a bounded integer environment variable safely."""
    raw_value = os.getenv(name)
    if raw_value is None:
        return default

    try:
        value = int(raw_value)
    except ValueError:
        return default

    return max(minimum, min(value, maximum))


@dataclass(frozen=True, slots=True)
class Settings:
    """Runtime limits and external OCR configuration."""

    tesseract_cmd: str | None = None
    ocr_language: str = "eng"
    default_timeout_seconds: int = 3
    max_timeout_seconds: int = 10
    max_upload_bytes: int = 5 * 1024 * 1024
    max_image_pixels: int = 16_000_000
    max_source_bytes: int = 50_000
    max_stdin_bytes: int = 64 * 1024
    max_output_bytes: int = 64 * 1024
    code_memory_limit_mb: int = 128

    @classmethod
    def from_environment(cls) -> "Settings":
        """Create settings from the process environment with safe bounds."""
        # This service owns the adjacent .env file. ``override=False`` ensures
        # container, CI, and process-level variables remain authoritative.
        load_dotenv(Path(__file__).resolve().parent.parent / ".env", override=False)
        return cls(
            tesseract_cmd=os.getenv("TESSERACT_CMD") or None,
            ocr_language=os.getenv("OCR_LANGUAGE", "eng"),
            default_timeout_seconds=_bounded_int(
                "CODE_TIMEOUT_SECONDS", default=3, minimum=1, maximum=10
            ),
            max_timeout_seconds=_bounded_int(
                "MAX_CODE_TIMEOUT_SECONDS", default=10, minimum=1, maximum=30
            ),
            max_upload_bytes=_bounded_int(
                "MAX_UPLOAD_BYTES",
                default=5 * 1024 * 1024,
                minimum=1_024,
                maximum=25 * 1024 * 1024,
            ),
            max_image_pixels=_bounded_int(
                "MAX_IMAGE_PIXELS",
                default=16_000_000,
                minimum=100_000,
                maximum=64_000_000,
            ),
            max_source_bytes=_bounded_int(
                "MAX_SOURCE_BYTES", default=50_000, minimum=1_000, maximum=500_000
            ),
            max_stdin_bytes=_bounded_int(
                "MAX_STDIN_BYTES", default=64 * 1024, minimum=1_024, maximum=1_048_576
            ),
            max_output_bytes=_bounded_int(
                "MAX_OUTPUT_BYTES", default=64 * 1024, minimum=1_024, maximum=1_048_576
            ),
            code_memory_limit_mb=_bounded_int(
                "CODE_MEMORY_LIMIT_MB", default=128, minimum=32, maximum=1_024
            ),
        )
