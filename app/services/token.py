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


def sign_token(file_id: str, title: str | None = None) -> str:
    expire = datetime.now(timezone.utc) + timedelta(seconds=_ttl)
    claims: dict = {"file_id": file_id, "exp": expire}
    if title:
        claims["title"] = title
    return jwt.encode(claims, _secret, algorithm=_algorithm)


def verify_token(token: str) -> tuple[str, str | None]:
    try:
        payload = jwt.decode(token, _secret, algorithms=[_algorithm])
        return payload["file_id"], payload.get("title")
    except ExpiredSignatureError:
        raise TokenExpiredError("Token has expired")
    except JWTError:
        raise TokenInvalidError("Token is invalid")
