import os
import shutil
from datetime import datetime, timezone

from dotenv import load_dotenv
from fastapi import FastAPI, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse

from database import SessionLocal
from models import Download, Request
from utils import generate_public_id
import tasks

load_dotenv()

UPLOAD_FOLDER = os.getenv("UPLOAD_FOLDER") or ""
DOWNLOAD_FOLDER = os.getenv("DOWNLOAD_FOLDER") or ""

if UPLOAD_FOLDER == "" or DOWNLOAD_FOLDER == "":
    raise Exception("The environment variables UPLOAD_FOLDER and DOWNLOAD_FOLDER must be specified")

ROMS_FOLDER = os.path.join(DOWNLOAD_FOLDER, "roms")

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
    request_id = generate_public_id()
    save_folder = os.path.join(UPLOAD_FOLDER, str(request_id))

    os.makedirs(save_folder, exist_ok=True)

    for file_upload in file_uploads:
        if file_upload.filename:
            save_path = os.path.join(save_folder, file_upload.filename)

            with open(save_path, "wb") as save_file:
                shutil.copyfileobj(file_upload.file, save_file)

    os.makedirs(ROMS_FOLDER, exist_ok=True)
    tasks.convert_to_chd.delay(save_folder, ROMS_FOLDER, request_id)

    datetime_now = datetime.now(timezone.utc)

    session.add(Request(public_id=request_id, type_id=1, status="pending", created_at=datetime_now, updated_at=datetime_now))
    session.commit()
    session.close()

    return {"request_id": request_id}

@app.get("/status/{request_id}")
async def get_download_id(request_id: str):
    request = session.query(Request).filter_by(public_id=request_id).one_or_none()
    download = session.query(Download).filter_by(request_id=request_id).one_or_none()

    if request is None:
        return {"error": "Invalid request", "status": "error"}

    if download is None:
        return {"error": "Download key not ready yet", "status": str(request.status)}

    return {"download_id": download.public_id, "status": request.status}

@app.get("/download/{download_id}")
async def download_file(download_id: str, file: str | None = None):
    download_path = ROMS_FOLDER + download_id + "/"
    try:
        games = [f for f in os.listdir(download_path) if os.path.isfile(os.path.join(download_path, f))]
    except Exception:
        return {"error": "Invalid download id"}
    else:
        if file:
            return FileResponse(download_path + file, filename=file)
        return FileResponse(download_path + games[0], filename=games[0])
