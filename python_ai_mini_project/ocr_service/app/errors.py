"""Typed, API-safe exceptions used by the grading pipeline."""

from __future__ import annotations


class ServiceError(Exception):
    """An expected error that can be returned to an API client safely."""

    status_code = 500

    def __init__(self, message: str) -> None:
        super().__init__(message)
        self.message = message


class InvalidImageError(ServiceError):
    """Raised when an upload is not a usable image."""

    status_code = 422


class PayloadTooLargeError(ServiceError):
    """Raised before an upload can consume excessive service resources."""

    status_code = 413


class InputValidationError(ServiceError):
    """Raised for invalid grading request values."""

    status_code = 422


class OcrUnavailableError(ServiceError):
    """Raised when Tesseract cannot be invoked by this service."""

    status_code = 503

