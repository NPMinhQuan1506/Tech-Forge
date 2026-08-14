"""Bounded subprocess execution for OCR-extracted Python submissions.

This is defense-in-depth, not a complete security boundary. Production should
run this service in a non-privileged container/VM with no network and a
read-only filesystem. The limits here still contain normal mistakes such as
infinite loops, runaway memory use (on Unix), and excessive captured output.
"""

from __future__ import annotations

import os
import signal
import subprocess
import sys
import tempfile
import threading
from dataclasses import dataclass
from pathlib import Path
from typing import BinaryIO, Callable, Literal

from .config import Settings

try:  # ``resource`` is not available on Windows.
    import resource
except ImportError:  # pragma: no cover - exercised on Windows only
    resource = None  # type: ignore[assignment]


@dataclass(frozen=True, slots=True)
class ExecutionResult:
    """Observed result of a bounded Python subprocess."""

    stdout: str
    stderr: str
    exit_code: int | None
    timed_out: bool
    output_truncated: bool

    @property
    def succeeded(self) -> bool:
        """Return whether the child completed normally."""
        return not self.timed_out and self.exit_code == 0


def _set_limit(limit: int, soft: int, hard: int) -> None:
    """Set a resource limit without failing an otherwise valid execution."""
    if resource is None:
        return
    try:
        resource.setrlimit(limit, (soft, hard))
    except (OSError, ValueError):
        # A host can impose a stricter hard limit. Its stricter limit remains.
        pass


def _unix_preexec(settings: Settings, timeout_seconds: int) -> Callable[[], None]:
    """Create child-only Unix limits applied immediately before ``exec``."""
    memory_bytes = settings.code_memory_limit_mb * 1024 * 1024
    output_bytes = settings.max_output_bytes

    def apply_limits() -> None:
        # One extra CPU second lets Python flush a traceback after the wall-time
        # guard, while retaining a strict CPU ceiling.
        _set_limit(resource.RLIMIT_CPU, timeout_seconds + 1, timeout_seconds + 2)
        _set_limit(resource.RLIMIT_AS, memory_bytes, memory_bytes)
        _set_limit(resource.RLIMIT_FSIZE, output_bytes, output_bytes)
        _set_limit(resource.RLIMIT_NOFILE, 32, 32)
        if hasattr(resource, "RLIMIT_NPROC"):
            _set_limit(resource.RLIMIT_NPROC, 16, 16)

    return apply_limits


def _safe_environment() -> dict[str, str]:
    """Do not pass API credentials or other parent-process environment values."""
    environment = {
        "PYTHONIOENCODING": "utf-8",
        "PYTHONUNBUFFERED": "1",
        "PYTHONDONTWRITEBYTECODE": "1",
    }
    if os.name == "nt":
        # Windows process creation needs these system locations, but no user
        # secrets are copied into the child environment.
        for key in ("SYSTEMROOT", "WINDIR", "COMSPEC"):
            if value := os.environ.get(key):
                environment[key] = value
    return environment


class _BoundedOutputCollector:
    """Thread-safe, combined stdout/stderr collector with a hard byte cap."""

    def __init__(self, maximum_bytes: int) -> None:
        self._maximum_bytes = maximum_bytes
        self._stdout = bytearray()
        self._stderr = bytearray()
        self._total_bytes = 0
        self._lock = threading.Lock()
        self.output_truncated = False

    def append(self, stream: Literal["stdout", "stderr"], chunk: bytes) -> bool:
        """Store a chunk and return whether the configured cap remains intact."""
        with self._lock:
            remaining = self._maximum_bytes - self._total_bytes
            target = self._stdout if stream == "stdout" else self._stderr
            if remaining <= 0:
                self.output_truncated = True
                return False

            accepted = chunk[:remaining]
            target.extend(accepted)
            self._total_bytes += len(accepted)
            if len(accepted) != len(chunk):
                self.output_truncated = True
                return False

            return True

    def as_text(self) -> tuple[str, str]:
        """Decode collected output after reader threads have finished."""
        with self._lock:
            return (
                self._stdout.decode("utf-8", errors="replace"),
                self._stderr.decode("utf-8", errors="replace"),
            )


def _terminate_process(process: subprocess.Popen[bytes]) -> None:
    """Terminate a timed-out process and its Unix process group when possible."""
    try:
        if os.name == "posix":
            # ``start_new_session`` makes the child PID its process-group ID,
            # so this still works if the direct child has already exited while
            # a descendant is holding its stdout/stderr pipe open.
            os.killpg(process.pid, signal.SIGKILL)
        else:  # Windows does not expose a portable process-tree primitive here.
            process.kill()
    except (OSError, ProcessLookupError):
        pass


def _drain_stream(
    stream: BinaryIO,
    stream_name: Literal["stdout", "stderr"],
    collector: _BoundedOutputCollector,
    process: subprocess.Popen[bytes],
) -> None:
    """Drain one pipe so a submission cannot block or exceed output limits."""
    try:
        while chunk := stream.read(8_192):
            if not collector.append(stream_name, chunk):
                _terminate_process(process)
                return
    finally:
        stream.close()


def execute_python_code(
    code: str,
    test_input: str,
    timeout_seconds: int,
    settings: Settings,
) -> ExecutionResult:
    """Execute one submission in a temporary directory with bounded resources."""
    source_bytes = code.encode("utf-8")
    input_bytes = test_input.encode("utf-8")
    if len(source_bytes) > settings.max_source_bytes:
        raise ValueError("Extracted source code exceeds the configured size limit.")
    if len(input_bytes) > settings.max_stdin_bytes:
        raise ValueError("Test input exceeds the configured size limit.")

    with tempfile.TemporaryDirectory(prefix="ocr_grader_") as temporary_directory:
        working_directory = Path(temporary_directory)
        source_path = working_directory / "submission.py"
        input_path = working_directory / "input.txt"
        source_path.write_text(code, encoding="utf-8")
        input_path.write_bytes(input_bytes)

        popen_kwargs: dict[str, object] = {
            "args": [sys.executable, "-I", "-B", str(source_path)],
            "cwd": str(working_directory),
            "env": _safe_environment(),
        }
        if os.name == "posix":
            popen_kwargs["preexec_fn"] = _unix_preexec(settings, timeout_seconds)
            popen_kwargs["start_new_session"] = True
        else:  # pragma: no cover - platform-specific process flags
            creation_flags = getattr(subprocess, "CREATE_NO_WINDOW", 0)
            creation_flags |= getattr(subprocess, "CREATE_NEW_PROCESS_GROUP", 0)
            popen_kwargs["creationflags"] = creation_flags

        try:
            with input_path.open("rb") as input_file:
                popen_kwargs["stdin"] = input_file
                popen_kwargs["stdout"] = subprocess.PIPE
                popen_kwargs["stderr"] = subprocess.PIPE
                process: subprocess.Popen[bytes] = subprocess.Popen(
                    **popen_kwargs  # type: ignore[arg-type]
                )
                if process.stdout is None or process.stderr is None:
                    raise RuntimeError("Could not capture Python sandbox output.")

                collector = _BoundedOutputCollector(settings.max_output_bytes)
                stdout_thread = threading.Thread(
                    target=_drain_stream,
                    args=(process.stdout, "stdout", collector, process),
                    daemon=True,
                )
                stderr_thread = threading.Thread(
                    target=_drain_stream,
                    args=(process.stderr, "stderr", collector, process),
                    daemon=True,
                )
                stdout_thread.start()
                stderr_thread.start()
                timed_out = False
                try:
                    process.wait(timeout=timeout_seconds)
                except subprocess.TimeoutExpired:
                    timed_out = True
                    _terminate_process(process)
                finally:
                    if process.poll() is None:
                        _terminate_process(process)
                    try:
                        process.wait(timeout=1)
                    except subprocess.TimeoutExpired:
                        _terminate_process(process)

                    stdout_thread.join(timeout=1)
                    stderr_thread.join(timeout=1)
                    if stdout_thread.is_alive() or stderr_thread.is_alive():
                        _terminate_process(process)
                        stdout_thread.join(timeout=1)
                        stderr_thread.join(timeout=1)
        except OSError as error:
            raise RuntimeError(
                f"Could not start the Python sandbox: {error}"
            ) from error

        stdout, stderr = collector.as_text()
        return ExecutionResult(
            stdout=stdout,
            stderr=stderr,
            exit_code=None if timed_out else process.returncode,
            timed_out=timed_out,
            output_truncated=collector.output_truncated,
        )
