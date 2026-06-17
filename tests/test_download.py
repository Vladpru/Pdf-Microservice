import pytest
from pathlib import Path
from app.services.token import sign_token


def _write_tmp_file(file_id: str, content: bytes = b"%PDF-fake") -> Path:
    from app.routers.generate import _tmp_dir
    path = _tmp_dir / f"{file_id}.pdf"
    path.write_bytes(content)
    return path


def test_download_valid_token(client, set_env):
    import uuid
    file_id = str(uuid.uuid4())
    _write_tmp_file(file_id)
    token = sign_token(file_id)

    response = client.get(f"/pdf/{token}")
    assert response.status_code == 200
    assert response.headers["content-type"] == "application/pdf"


def test_download_invalid_token(client, set_env):
    response = client.get("/pdf/not.a.valid.token")
    assert response.status_code == 401


def test_download_expired_token(client, monkeypatch, set_env):
    import app.services.token as token_module
    import time
    monkeypatch.setattr(token_module, "_ttl", 0)
    import uuid
    file_id = str(uuid.uuid4())
    _write_tmp_file(file_id)
    token = sign_token(file_id)
    time.sleep(1)

    response = client.get(f"/pdf/{token}")
    assert response.status_code == 401


def test_download_missing_file(client, set_env):
    token = sign_token("nonexistent-file-id")
    response = client.get(f"/pdf/{token}")
    assert response.status_code == 410
