from datetime import datetime, timezone, timedelta
from jose import jwt, JWTError, ExpiredSignatureError
from app.config import settings

_ttl = settings.token_ttl_seconds
_secret = settings.pdf_service_secret
_algorithm = "HS256"


class TokenExpiredError(Exception):
    pass


class TokenInvalidError(Exception):
    pass


def sign_token(file_id: str) -> str:
    expire = datetime.now(timezone.utc) + timedelta(seconds=_ttl)
    return jwt.encode({"file_id": file_id, "exp": expire}, _secret, algorithm=_algorithm)


def verify_token(token: str) -> str:
    try:
        payload = jwt.decode(token, _secret, algorithms=[_algorithm])
        return payload["file_id"]
    except ExpiredSignatureError:
        raise TokenExpiredError("Token has expired")
    except JWTError:
        raise TokenInvalidError("Token is invalid")
