"""Shared FastAPI test setup."""

from __future__ import annotations

import pytest
from fastapi.testclient import TestClient

from app.config import Settings
from app.main import app, get_settings


@pytest.fixture()
def settings() -> Settings:
    """Small deterministic limits appropriate for tests."""
    return Settings(
        default_timeout_seconds=2,
        max_timeout_seconds=5,
        max_upload_bytes=1_024 * 1_024,
        max_image_pixels=1_000_000,
        max_source_bytes=10_000,
        max_stdin_bytes=1_024,
        max_output_bytes=1_024,
        code_memory_limit_mb=64,
    )


@pytest.fixture()
def client(settings: Settings):
    """TestClient with deterministic dependency-injected settings."""
    app.dependency_overrides[get_settings] = lambda: settings
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()
