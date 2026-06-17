from pathlib import Path
from fastapi import APIRouter, HTTPException, BackgroundTasks
from fastapi.responses import FileResponse
from app.services.token import verify_token, TokenExpiredError, TokenInvalidError

router = APIRouter()

_tmp_dir = Path("/tmp/pdf-service")


def _delete_file(path: Path):
    try:
        path.unlink(missing_ok=True)
    except Exception:
        pass


@router.get("/pdf/{token}")
def download(token: str, background_tasks: BackgroundTasks):
    try:
        file_id = verify_token(token)
    except TokenExpiredError:
        raise HTTPException(status_code=401, detail="Download link has expired")
    except TokenInvalidError:
        raise HTTPException(status_code=401, detail="Invalid download link")

    file_path = _tmp_dir / f"{file_id}.pdf"
    if not file_path.exists():
        raise HTTPException(status_code=410, detail="File no longer available")

    background_tasks.add_task(_delete_file, file_path)

    return FileResponse(
        path=str(file_path),
        media_type="application/pdf",
        filename=f"export-{file_id[:8]}.pdf",
    )
