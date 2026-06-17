import os
import pytest
from fastapi.testclient import TestClient

# Set defaults before any test module is imported during collection
os.environ.setdefault("PDF_SERVICE_SECRET", "test-secret-32-chars-minimum-ok!")
os.environ.setdefault("PDF_INTERNAL_SECRET", "internal-secret")


@pytest.fixture(autouse=True)
def set_env(monkeypatch):
    monkeypatch.setenv("PDF_SERVICE_SECRET", "test-secret-32-chars-minimum-ok!")
    monkeypatch.setenv("PDF_INTERNAL_SECRET", "internal-secret")


@pytest.fixture
def client():
    from app.main import app
    return TestClient(app)
