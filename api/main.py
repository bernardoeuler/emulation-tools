import os
import shutil
import uuid
from datetime import datetime, timezone
from pathlib import Path

from dotenv import load_dotenv
from fastapi import FastAPI, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse

from database.session import SessionLocal
from database.models import Download, Request, RequestStatusEnum, RequestTypeEnum, DownloadStatusEnum
import app.utils.tasks as tasks

load_dotenv()

UPLOAD_FOLDER = Path(os.getenv("UPLOAD_FOLDER", "uploads"))
DOWNLOAD_FOLDER = Path(os.getenv("DOWNLOAD_FOLDER", "downloads"))

app = FastAPI()
session = SessionLocal()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/upload/")
async def upload(file_uploads: list[UploadFile]):
    request_id = uuid.uuid4().hex
    save_folder = UPLOAD_FOLDER / request_id

    save_folder.mkdir(parents=True, exist_ok=True)

    for file_upload in file_uploads:
        if file_upload.filename:
            save_path = save_folder / file_upload.filename

            with open(save_path, "wb") as save_file:
                shutil.copyfileobj(file_upload.file, save_file)

    session.add(Request(public_id=request_id, type=RequestTypeEnum.ROM_CONVERSION, status=RequestStatusEnum.PENDING, created_at=datetime.now(timezone.utc), updated_at=datetime.now(timezone.utc)))

    session.commit()
    session.close()

    tasks.convert_to_chd.delay(str(save_folder), request_id)

    return {"request_id": request_id}

@app.get("/status/{request_id}")
async def get_status(request_id: str):
    request = session.query(Request).filter_by(public_id=request_id).one_or_none()

    if request is None:
        return {"error": "Request not found"}

    download = session.query(Download).filter_by(request_id=request.id).one_or_none()

    if download is None:
        return {"error": "Download not ready yet"}

    return {"download_id": download.public_id, "status": download.status}

@app.get("/download/{download_id}")
async def download_file(download_id: str, file: str | None = None):
    download = session.query(Download).filter_by(public_id=download_id).one_or_none()

    if download is None or download.status != DownloadStatusEnum.READY:
        return {"error": "Download not ready"}

    download_path = DOWNLOAD_FOLDER / download.public_id

    try:
        files = [f.name for f in download_path.iterdir() if f.is_file()]
    except Exception:
        return {"error": "Could not access download files"}

    if not files:
        return {"error": "No files available for download"}

    if file:
        filename = file
    else:
        filename = files[0]

    return FileResponse(download_path / filename, filename=filename, headers={"Content-Type": "application/zip"})
