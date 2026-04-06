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

current_folder = Path(__file__).resolve().parent

UPLOAD_FOLDER = os.getenv("UPLOAD_FOLDER") or current_folder.as_posix() + "/user-uploads/"
DOWNLOAD_FOLDER = os.getenv("DOWNLOAD_FOLDER") or current_folder.as_posix() + "/user-downloads/"

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
    save_folder = UPLOAD_FOLDER + str(request_id) + "/"

    os.makedirs(save_folder, exist_ok=True)

    for file_upload in file_uploads:
        if file_upload.filename:
            save_path = save_folder + file_upload.filename

            with open(save_path, "wb") as save_file:
                shutil.copyfileobj(file_upload.file, save_file)

    session.add(Request(public_id=request_id, type=RequestTypeEnum.ROM_CONVERSION, status=RequestStatusEnum.PENDING, created_at=datetime.now(timezone.utc), updated_at=datetime.now(timezone.utc)))

    session.commit()
    session.close()

    tasks.convert_to_chd.delay(save_folder, request_id)

    return {"request_id": request_id}

@app.get("/status/{request_id}")
async def get_download_id(request_id: str):
    request = session.query(Request).filter_by(public_id=request_id).one_or_none()

    if request is None:
        return {"error": "Invalid request"}

    download = session.query(Download).filter_by(request_id=request.id).one_or_none()

    if download is None:
        return {"error": "Download has not been started yet"}

    return {"download_id": download.public_id, "status": download.status}

@app.get("/download/{download_id}")
async def download_file(download_id: str, file: str | None = None):
    download = session.query(Download).filter_by(public_id=download_id).one_or_none()

    if download is None or download.status != DownloadStatusEnum.READY:
        return {"error": "Download not ready yet"}

    download_path = DOWNLOAD_FOLDER + download.public_id + "/"

    try:
        games = [f for f in os.listdir(download_path) if os.path.isfile(os.path.join(download_path, f))]
    except Exception:
        return {"error": "Could not download files. Download may have expired."}
    else:
        headers = {"Content-Type": "application/zip"}

        if file:
            return FileResponse(download_path + file, filename=file, headers=headers)
        return FileResponse(download_path + games[0], filename=games[0], headers=headers)
