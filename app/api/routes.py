from pathlib import Path
from typing import Annotated, Optional

import httpx
from fastapi import APIRouter, File, Form, HTTPException, UploadFile
from fastapi.responses import JSONResponse

from app.core.config import settings
from app.services.parser import DocumentParser, cleanup_files

router = APIRouter()


def _save_upload(upload: UploadFile, target: Path) -> None:
    with target.open("wb") as handle:
        for chunk in iter(lambda: upload.file.read(1024 * 1024), b""):
            handle.write(chunk)


def _enforce_size_limit(target: Path) -> None:
    max_bytes = settings.max_upload_mb * 1024 * 1024
    if target.stat().st_size > max_bytes:
        raise HTTPException(status_code=413, detail="File too large")


def _download_to(url: str, target: Path) -> None:
    with httpx.stream("GET", url, timeout=30.0, follow_redirects=True) as response:
        if response.status_code >= 400:
            raise HTTPException(status_code=400, detail="Failed to download PDF")
        with target.open("wb") as handle:
            for chunk in response.iter_bytes(chunk_size=1024 * 1024):
                handle.write(chunk)


@router.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "ok"}


@router.post("/parse")
def parse_pdf(
    file: Annotated[Optional[UploadFile], File()] = None,
    url: Annotated[Optional[str], Form()] = None,
) -> JSONResponse:
    if not file and not url:
        raise HTTPException(status_code=400, detail="Provide file or url")
    if file and url:
        raise HTTPException(status_code=400, detail="Provide only one input")

    temp_dir = Path(settings.temp_dir)
    temp_dir.mkdir(parents=True, exist_ok=True)
    cleanup: list[Path] = []

    try:
        if file:
            if file.content_type not in {"application/pdf"}:
                raise HTTPException(status_code=400, detail="Only PDF files supported")
            target = temp_dir / file.filename if file.filename else temp_dir / "upload.pdf"
            _save_upload(file, target)
            _enforce_size_limit(target)
        else:
            target = temp_dir / "download.pdf"
            _download_to(url, target)
            _enforce_size_limit(target)

        cleanup.append(target)
        parser = DocumentParser()
        markdown = parser.parse(target)
    finally:
        cleanup_files(cleanup)

    return JSONResponse({"markdown": markdown})
