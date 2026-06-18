import uuid
from datetime import datetime, timezone, timedelta
from pathlib import Path
from typing import Optional
from fastapi import APIRouter, HTTPException, Header
from app.schemas.payload import EntityPayload, GenerateResponse
from app.services.pdf import render_pdf
from app.services.token import sign_token
from app.config import settings

router = APIRouter()

_tmp_dir = Path("/tmp/pdf-service")
_tmp_dir.mkdir(exist_ok=True)


def _verify_internal_auth(authorization: Optional[str]):
    expected = f"Bearer {settings.pdf_internal_secret}"
    if authorization != expected:
        raise HTTPException(status_code=401, detail="Unauthorized")


@router.post("/generate", response_model=GenerateResponse)
def generate(
    payload: EntityPayload,
    authorization: Optional[str] = Header(default=None),
):
    _verify_internal_auth(authorization)

    pdf_bytes = render_pdf(payload)

    file_id = str(uuid.uuid4())
    file_path = _tmp_dir / f"{file_id}.pdf"
    file_path.write_bytes(pdf_bytes)

    token = sign_token(file_id, title=payload.title)
    expires_at = datetime.now(timezone.utc) + timedelta(seconds=settings.token_ttl_seconds)

    download_url = f"{settings.pdf_service_base_url}/pdf/{token}"

    return GenerateResponse(download_url=download_url, expires_at=expires_at)
