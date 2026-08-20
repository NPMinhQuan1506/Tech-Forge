"""HTTP-contract tests; OCR and execution are mocked independently."""

from __future__ import annotations

from unittest.mock import patch

from app.ocr import OcrExtraction
from app.sandbox import ExecutionResult


def test_health_check(client) -> None:
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok", "service": "ocr-grader"}


def test_grade_image_returns_passed_contract(client) -> None:
    extraction = OcrExtraction(code="print('Hello')", confidence=98.2)
    execution = ExecutionResult(
        stdout="Hello\n",
        stderr="",
        exit_code=0,
        timed_out=False,
        output_truncated=False,
    )
    with patch("app.main.extract_python_code", return_value=extraction), patch(
        "app.main.execute_python_code", return_value=execution
    ):
        response = client.post(
            "/api/v1/grade-image",
            files={"image": ("code.png", b"fake image bytes", "image/png")},
            data={
                "expected_output": "Hello",
                "test_input": "",
                "timeout_seconds": "2",
            },
        )

    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "passed"
    assert body["extracted_code"] == "print('Hello')"
    assert body["ocr_confidence"] == 98.2
    assert body["execution_output"] == "Hello\n"
    assert body["error_message"] is None


def test_grade_image_returns_failed_for_wrong_output(client) -> None:
    extraction = OcrExtraction(code="print('wrong')", confidence=77.0)
    execution = ExecutionResult(
        stdout="wrong\n",
        stderr="",
        exit_code=0,
        timed_out=False,
        output_truncated=False,
    )
    with patch("app.main.extract_python_code", return_value=extraction), patch(
        "app.main.execute_python_code", return_value=execution
    ):
        response = client.post(
            "/api/v1/grade-image",
            files={"image": ("code.png", b"fake image bytes", "image/png")},
            data={"expected_output": "correct"},
        )

    assert response.status_code == 200
    assert response.json()["status"] == "failed"
    assert "does not match" in response.json()["error_message"]


def test_grade_image_rejects_oversized_file(client, settings) -> None:
    response = client.post(
        "/api/v1/grade-image",
        files={
            "image": (
                "code.png",
                b"a" * (settings.max_upload_bytes + 1),
                "image/png",
            )
        },
        data={"expected_output": "anything"},
    )

    assert response.status_code == 413
    assert response.json()["status"] == "error"


def test_grade_image_returns_contract_for_missing_required_field(client) -> None:
    response = client.post(
        "/api/v1/grade-image",
        files={"image": ("code.png", b"fake image bytes", "image/png")},
    )

    assert response.status_code == 422
    body = response.json()
    assert body["status"] == "error"
    assert body["extracted_code"] == ""
    assert body["error_message"]


def test_grade_image_rejects_zero_timeout(client) -> None:
    response = client.post(
        "/api/v1/grade-image",
        files={"image": ("code.png", b"fake image bytes", "image/png")},
        data={"expected_output": "unused", "timeout_seconds": "0"},
    )

    assert response.status_code == 422
    assert "timeout_seconds" in response.json()["error_message"]


def test_run_code_returns_execution_output(client) -> None:
    execution = ExecutionResult(
        stdout="Hello sandbox\n",
        stderr="",
        exit_code=0,
        timed_out=False,
        output_truncated=False,
    )
    with patch("app.main.execute_python_code", return_value=execution) as mock_execute:
        response = client.post(
            "/api/v1/run-code",
            json={
                "code": "print('Hello sandbox')",
                "stdin": "",
                "timeout_seconds": 2,
            },
        )

    assert response.status_code == 200
    assert response.json()["status"] == "passed"
    assert response.json()["execution_output"] == "Hello sandbox\n"
    mock_execute.assert_called_once()


def test_run_code_returns_error_for_runtime_failure(client) -> None:
    execution = ExecutionResult(
        stdout="",
        stderr="ValueError: bad input\n",
        exit_code=1,
        timed_out=False,
        output_truncated=False,
    )
    with patch("app.main.execute_python_code", return_value=execution):
        response = client.post(
            "/api/v1/run-code",
            json={"code": "raise ValueError('bad input')"},
        )

    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "error"
    assert "ValueError" in body["error_message"]


def test_run_code_rejects_empty_code(client) -> None:
    response = client.post("/api/v1/run-code", json={"code": ""})

    assert response.status_code == 422
    assert response.json()["status"] == "error"
