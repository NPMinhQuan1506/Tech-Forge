"""HTTP API for receiving a code photograph and returning a grade."""

from __future__ import annotations

import logging
from functools import lru_cache

from fastapi import Depends, FastAPI, File, Form, UploadFile
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from .config import Settings
from .errors import (
    InputValidationError,
    InvalidImageError,
    PayloadTooLargeError,
    ServiceError,
)
from .ocr import extract_python_code
from .sandbox import ExecutionResult, execute_python_code
from .schemas import CodeRunRequest, CodeRunResponse, GradeImageResponse, GradeStatus, HealthResponse

logger = logging.getLogger(__name__)

app = FastAPI(
    title="Python Learning Platform OCR Grader",
    version="1.0.0",
    docs_url="/docs",
    redoc_url=None,
)


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    """Build settings once per service process; tests can override this dependency."""
    return Settings.from_environment()


def _normalise_output(value: str) -> str:
    """Compare output portably while ignoring only final line terminators."""
    return value.replace("\r\n", "\n").replace("\r", "\n").rstrip("\n")


def _failure_message(execution: ExecutionResult) -> str | None:
    """Produce an actionable failure reason without hiding student stderr."""
    if execution.timed_out:
        return "The code exceeded the execution time limit."
    if execution.stderr.strip():
        return execution.stderr.strip()
    if execution.exit_code not in (None, 0):
        return f"The code exited with status {execution.exit_code}."
    return None


@app.exception_handler(ServiceError)
async def service_error_handler(_, error: ServiceError) -> JSONResponse:
    """Keep expected API errors in the same contract Django consumes."""
    body = GradeImageResponse(
        status=GradeStatus.ERROR,
        error_message=error.message,
    )
    return JSONResponse(
        status_code=error.status_code,
        content=body.model_dump(mode="json"),
    )


@app.exception_handler(RequestValidationError)
async def request_validation_error_handler(
    _,
    error: RequestValidationError,
) -> JSONResponse:
    """Return malformed multipart requests in Django's stable response shape."""
    first_error = error.errors()[0] if error.errors() else {}
    location = ".".join(
        str(item) for item in first_error.get("loc", []) if item != "body"
    )
    message = first_error.get("msg", "Invalid request data.")
    error_message = f"{location}: {message}" if location else message
    body = GradeImageResponse(
        status=GradeStatus.ERROR,
        error_message=error_message,
    )
    return JSONResponse(status_code=422, content=body.model_dump(mode="json"))


@app.exception_handler(Exception)
async def unexpected_error_handler(_, error: Exception) -> JSONResponse:
    """Avoid exposing server traces while preserving an observable server log."""
    logger.exception("Unexpected error while grading image", exc_info=error)
    body = GradeImageResponse(
        status=GradeStatus.ERROR,
        error_message="The grading service encountered an unexpected error.",
    )
    return JSONResponse(status_code=500, content=body.model_dump(mode="json"))


@app.get("/health", response_model=HealthResponse)
async def health_check() -> HealthResponse:
    """Return liveness without requiring a sample image or running Tesseract."""
    return HealthResponse()


@app.post("/api/v1/grade-image", response_model=GradeImageResponse)
async def grade_image(
    image: UploadFile = File(
        ...,
        description="Photo or screenshot containing Python code",
    ),
    expected_output: str = Form(..., description="Expected stdout for the exercise"),
    test_input: str | None = Form(
        None,
        description="Optional stdin supplied to the code",
    ),
    timeout_seconds: int | None = Form(
        None,
        description="Requested execution limit in seconds",
    ),
    settings: Settings = Depends(get_settings),
) -> GradeImageResponse:
    """OCR the submitted code, execute it with limits, and compare stdout."""
    if image.content_type and not image.content_type.startswith("image/"):
        raise InvalidImageError("The uploaded file must have an image content type.")

    try:
        image_bytes = await image.read(settings.max_upload_bytes + 1)
    finally:
        await image.close()

    if len(image_bytes) > settings.max_upload_bytes:
        raise PayloadTooLargeError("The uploaded image exceeds the size limit.")

    requested_timeout = (
        settings.default_timeout_seconds if timeout_seconds is None else timeout_seconds
    )
    if requested_timeout < 1 or requested_timeout > settings.max_timeout_seconds:
        raise InputValidationError(
            f"timeout_seconds must be between 1 and {settings.max_timeout_seconds}."
        )

    supplied_input = test_input or ""
    if len(supplied_input.encode("utf-8")) > settings.max_stdin_bytes:
        raise InputValidationError("test_input exceeds the configured size limit.")
    if len(expected_output.encode("utf-8")) > settings.max_output_bytes:
        raise InputValidationError("expected_output exceeds the configured size limit.")

    extraction = extract_python_code(image_bytes, settings)
    try:
        execution = execute_python_code(
            code=extraction.code,
            test_input=supplied_input,
            timeout_seconds=requested_timeout,
            settings=settings,
        )
    except (ValueError, RuntimeError) as error:
        logger.warning("Sandbox setup rejected a grading request: %s", error)
        return GradeImageResponse(
            status=GradeStatus.ERROR,
            extracted_code=extraction.code,
            ocr_confidence=extraction.confidence,
            error_message=str(error),
        )

    output_matches = _normalise_output(execution.stdout) == _normalise_output(
        expected_output
    )
    passed = execution.succeeded and output_matches and not execution.output_truncated
    failure_message = None if passed else _failure_message(execution)
    if not passed and failure_message is None:
        failure_message = "Program output does not match the expected output."
    if execution.output_truncated:
        failure_message = "Program output exceeded the configured output limit."

    return GradeImageResponse(
        status=GradeStatus.PASSED if passed else GradeStatus.FAILED,
        extracted_code=extraction.code,
        ocr_confidence=extraction.confidence,
        execution_output=execution.stdout,
        error_message=failure_message,
        exit_code=execution.exit_code,
        timed_out=execution.timed_out,
        output_truncated=execution.output_truncated,
    )


@app.post("/api/v1/run-code", response_model=CodeRunResponse)
async def run_code(
    request: CodeRunRequest,
    settings: Settings = Depends(get_settings),
) -> CodeRunResponse:
    """Execute typed practice code without OCR, using the same sandbox limits."""
    if request.timeout_seconds > settings.max_timeout_seconds:
        raise InputValidationError(
            f"timeout_seconds must be between 1 and {settings.max_timeout_seconds}."
        )
    if len(request.stdin.encode("utf-8")) > settings.max_stdin_bytes:
        raise InputValidationError("stdin exceeds the configured size limit.")

    try:
        execution = execute_python_code(
            code=request.code,
            test_input=request.stdin,
            timeout_seconds=request.timeout_seconds,
            settings=settings,
        )
    except (ValueError, RuntimeError) as error:
        logger.warning("Sandbox setup rejected a direct run request: %s", error)
        return CodeRunResponse(
            status=GradeStatus.ERROR,
            error_message=str(error),
        )

    failure_message = None if execution.succeeded else _failure_message(execution)
    if execution.output_truncated:
        failure_message = "Program output exceeded the configured output limit."

    return CodeRunResponse(
        status=GradeStatus.PASSED if execution.succeeded else GradeStatus.ERROR,
        execution_output=execution.stdout,
        error_message=failure_message,
        exit_code=execution.exit_code,
        timed_out=execution.timed_out,
        output_truncated=execution.output_truncated,
    )
