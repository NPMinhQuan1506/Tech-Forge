"""Pydantic response models for the public API."""

from __future__ import annotations

from enum import Enum

from pydantic import BaseModel, Field


class GradeStatus(str, Enum):
    """The result category sent to the Django caller."""

    PASSED = "passed"
    FAILED = "failed"
    ERROR = "error"


class HealthResponse(BaseModel):
    """Liveness response; it avoids running a costly OCR operation."""

    status: str = "ok"
    service: str = "ocr-grader"


class GradeImageResponse(BaseModel):
    """Stable Django-to-FastAPI grading response contract."""

    status: GradeStatus
    extracted_code: str = ""
    ocr_confidence: float | None = Field(default=None, ge=0, le=100)
    execution_output: str = ""
    error_message: str | None = None

    # Extra diagnostics are intentionally additive; Django only depends on the
    # five fields above and can safely ignore these fields.
    exit_code: int | None = None
    timed_out: bool = False
    output_truncated: bool = False


class CodeRunRequest(BaseModel):
    """Direct code execution contract used by Django's practice sandbox."""

    code: str = Field(..., min_length=1, max_length=50_000)
    stdin: str = Field(default="", max_length=64 * 1024)
    timeout_seconds: int = Field(default=3, ge=1, le=10)


class CodeRunResponse(BaseModel):
    """Stable response for interactive practice runs."""

    status: GradeStatus
    execution_output: str = ""
    error_message: str | None = None
    exit_code: int | None = None
    timed_out: bool = False
    output_truncated: bool = False
