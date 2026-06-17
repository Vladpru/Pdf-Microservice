import time
import pytest
from app.services.token import sign_token, verify_token, TokenExpiredError, TokenInvalidError


def test_sign_and_verify(set_env):
    file_id = "abc-123"
    token = sign_token(file_id)
    assert isinstance(token, str)
    assert verify_token(token) == file_id


def test_expired_token(monkeypatch, set_env):
    import app.services.token as token_module
    monkeypatch.setattr(token_module, "_ttl", 0)
    token = sign_token("abc-123")
    time.sleep(1)
    with pytest.raises(TokenExpiredError):
        verify_token(token)


def test_invalid_token(set_env):
    with pytest.raises(TokenInvalidError):
        verify_token("not.a.valid.token")
