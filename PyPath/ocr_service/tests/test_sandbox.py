"""Tests for real bounded execution and mocked process-start errors."""

from __future__ import annotations

from dataclasses import replace
from unittest.mock import patch

import pytest

from app.sandbox import execute_python_code


def test_executes_simple_python_program(settings) -> None:
    result = execute_python_code("print(input().upper())", "hello\n", 2, settings)

    assert result.succeeded is True
    assert result.stdout.replace("\r\n", "\n") == "HELLO\n"
    assert result.stderr == ""


def test_timeout_is_reported(settings) -> None:
    result = execute_python_code("while True: pass", "", 1, settings)

    assert result.timed_out is True
    assert result.succeeded is False
    assert result.exit_code is None


def test_output_limit_is_enforced(settings) -> None:
    limited_settings = replace(settings, max_output_bytes=20)
    result = execute_python_code("print('x' * 100)", "", 2, limited_settings)

    assert result.output_truncated is True
    assert len(result.stdout.encode("utf-8")) <= 20


def test_subprocess_start_failure_is_wrapped(settings) -> None:
    with patch("app.sandbox.subprocess.Popen", side_effect=OSError("blocked")):
        with pytest.raises(RuntimeError, match="Could not start the Python sandbox"):
            execute_python_code("print('x')", "", 1, settings)
