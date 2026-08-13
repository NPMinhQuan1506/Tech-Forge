"""Client and orchestration code for the isolated FastAPI grading service."""

from __future__ import annotations

import logging
import math
import mimetypes
from dataclasses import dataclass
from typing import Any

import requests
from django.conf import settings
from django.db import transaction

from .models import Submission


logger = logging.getLogger(__name__)


class GradingServiceError(Exception):
    """Raised when the OCR/grading service cannot produce a usable result."""


@dataclass(frozen=True)
class GradeResult:
    """Normalized response returned from the FastAPI OCR/grading contract."""

    status: str
    extracted_code: str
    ocr_confidence: float | None
    execution_output: str
    error_message: str
    raw_response: dict[str, Any]


@dataclass(frozen=True)
class CodeRunResult:
    """Normalized response returned from the FastAPI direct sandbox."""

    status: str
    execution_output: str
    error_message: str
    exit_code: int | None
    timed_out: bool
    output_truncated: bool
    raw_response: dict[str, Any]


class FastAPIGraderClient:
    """Small synchronous HTTP client for the FastAPI OCR/sandbox endpoint."""

    def __init__(self, url: str | None = None, timeout: int | None = None) -> None:
        self.url = url or settings.FASTAPI_OCR_URL
        self.timeout = timeout or settings.FASTAPI_TIMEOUT_SECONDS

    def grade(self, submission: Submission) -> GradeResult:
        """Send an image and its exercise contract to FastAPI for grading."""
        if not submission.image:
            raise GradingServiceError("The submission has no image to process.")

        try:
            with submission.image.open("rb") as image_file:
                files = {
                    "image": (
                        submission.image.name.rsplit("/", 1)[-1],
                        image_file,
                        mimetypes.guess_type(submission.image.name)[0]
                        or "application/octet-stream",
                    )
                }
                data = {
                    "expected_output": submission.exercise.expected_output,
                    "test_input": submission.exercise.test_input,
                    "timeout_seconds": str(submission.exercise.timeout_seconds),
                }
                response = requests.post(
                    self.url,
                    files=files,
                    data=data,
                    timeout=self.timeout,
                )
        except (OSError, ValueError, requests.RequestException) as exc:
            raise GradingServiceError(
                "The OCR grading service is unavailable. Please try again shortly."
            ) from exc

        try:
            payload = response.json()
        except ValueError as exc:
            raise GradingServiceError(
                "The OCR grading service returned an invalid response."
            ) from exc

        if not isinstance(payload, dict):
            raise GradingServiceError(
                "The OCR grading service returned an invalid response."
            )

        # FastAPI deliberately returns a structured `status: error` payload for
        # OCR and validation failures, sometimes with a 4xx response code. Keep
        # that diagnostic on the learner's submission instead of discarding it.
        if response.status_code >= 400 and payload.get("status") != "error":
            try:
                response.raise_for_status()
            except requests.RequestException as exc:
                raise GradingServiceError(
                    "The OCR grading service is unavailable. Please try again shortly."
                ) from exc

        return self._normalize_payload(payload)

    @staticmethod
    def _normalize_payload(payload: dict[str, Any]) -> GradeResult:
        """Support the documented contract and safe boolean compatibility aliases."""
        status = str(payload.get("status", "")).lower()
        if status not in {"passed", "failed", "error"}:
            if payload.get("passed") is True or payload.get("success") is True:
                status = Submission.Status.PASSED
            elif payload.get("passed") is False:
                status = Submission.Status.FAILED
            else:
                status = Submission.Status.ERROR

        confidence = payload.get("ocr_confidence")
        try:
            confidence = float(confidence) if confidence is not None else None
        except (TypeError, ValueError):
            confidence = None
        if confidence is not None and not math.isfinite(confidence):
            confidence = None

        return GradeResult(
            status=status,
            extracted_code=str(payload.get("extracted_code") or ""),
            ocr_confidence=confidence,
            execution_output=str(
                payload.get("execution_output") or payload.get("output") or ""
            ),
            error_message=str(
                payload.get("error_message") or payload.get("detail") or ""
            ),
            raw_response=payload,
        )


class FastAPICodeRunnerClient:
    """HTTP client for typed practice code sent to FastAPI's sandbox."""

    def __init__(self, url: str | None = None, timeout: int | None = None) -> None:
        self.url = url or settings.FASTAPI_RUN_CODE_URL
        self.timeout = timeout or settings.FASTAPI_TIMEOUT_SECONDS

    def run(
        self,
        *,
        code: str,
        stdin: str = "",
        timeout_seconds: int = 3,
    ) -> CodeRunResult:
        try:
            response = requests.post(
                self.url,
                json={
                    "code": code,
                    "stdin": stdin,
                    "timeout_seconds": timeout_seconds,
                },
                timeout=self.timeout,
            )
            payload = response.json()
        except (ValueError, requests.RequestException) as exc:
            raise GradingServiceError(
                "The code sandbox is unavailable. Please try again shortly."
            ) from exc

        if not isinstance(payload, dict):
            raise GradingServiceError("The code sandbox returned an invalid response.")

        if response.status_code >= 400 and payload.get("status") != "error":
            try:
                response.raise_for_status()
            except requests.RequestException as exc:
                raise GradingServiceError(
                    "The code sandbox is unavailable. Please try again shortly."
                ) from exc

        return self._normalize_payload(payload)

    @staticmethod
    def _normalize_payload(payload: dict[str, Any]) -> CodeRunResult:
        status = str(payload.get("status", "")).lower()
        if status not in {"passed", "failed", "error"}:
            status = Submission.Status.ERROR

        try:
            exit_code = payload.get("exit_code")
            exit_code = int(exit_code) if exit_code is not None else None
        except (TypeError, ValueError):
            exit_code = None

        return CodeRunResult(
            status=status,
            execution_output=str(payload.get("execution_output") or ""),
            error_message=str(
                payload.get("error_message") or payload.get("detail") or ""
            ),
            exit_code=exit_code,
            timed_out=bool(payload.get("timed_out")),
            output_truncated=bool(payload.get("output_truncated")),
            raw_response=payload,
        )


def grade_submission(submission: Submission) -> Submission:
    """Call FastAPI, store its outcome, and turn transport faults into safe state."""
    submission.status = Submission.Status.PROCESSING
    submission.error_message = ""
    submission.save(update_fields=("status", "error_message", "updated_at"))

    try:
        result = FastAPIGraderClient().grade(submission)
    except GradingServiceError as exc:
        logger.warning("Submission %s could not be graded: %s", submission.id, exc)
        submission.status = Submission.Status.ERROR
        submission.error_message = str(exc)
        submission.save(update_fields=("status", "error_message", "updated_at"))
        return submission

    with transaction.atomic():
        submission.status = result.status
        submission.extracted_code = result.extracted_code
        submission.ocr_confidence = result.ocr_confidence
        submission.execution_output = result.execution_output
        submission.error_message = result.error_message
        submission.grader_response = result.raw_response
        submission.save(
            update_fields=(
                "status",
                "extracted_code",
                "ocr_confidence",
                "execution_output",
                "error_message",
                "grader_response",
                "updated_at",
            )
        )
    return submission
