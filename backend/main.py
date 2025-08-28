import os
import random
import shutil

from dotenv import load_dotenv
from fastapi import FastAPI, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse

import tasks

load_dotenv()

UPLOAD_FOLDER = os.getenv("UPLOAD_FOLDER")
DOWNLOAD_FOLDER = os.getenv("DOWNLOAD_FOLDER")
ROMS_FOLDER = DOWNLOAD_FOLDER + "roms/"

requests = {}

def generate_request_id():
    request_id = random.randint(10000000,99999999)

    while request_id in requests.keys():
        request_id = random.randint(10000000,99999999)

    requests[request_id] = {"status": "pending"}

    return request_id

def generate_download_key(request_id: int):
    key = random.randint(10000000,99999999)

    while key in [req["download_key"] for req in requests.values() if "download_key" in req]:
        key = random.randint(10000000,99999999)

    requests[request_id]["download_key"] = key

    return str(key)

def update_requests(request_id: int, new_status: str):
    requests[request_id]["status"] = new_status

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/upload/")
async def upload(file_uploads: list[UploadFile]):
    request_id = generate_request_id()
    download_key = generate_download_key(request_id)
    save_folder = UPLOAD_FOLDER + str(request_id) + "/"
    download_folder = ROMS_FOLDER + download_key

    os.makedirs(save_folder, exist_ok=True)
    os.makedirs(ROMS_FOLDER, exist_ok=True)

    for file_upload in file_uploads:
        if file_upload.filename:
            save_path = save_folder + file_upload.filename

            with open(save_path, "wb") as save_file:
                shutil.copyfileobj(file_upload.file, save_file)

    tasks.convert_to_chd.delay(save_folder, download_folder)

    return {"request_id": request_id}

@app.get("/status/{request_id}")
async def get_download_key(request_id: int):
    print(requests)

    if not requests or requests[request_id] is None:
        return {"error": "Invalid request"}

    if not requests or requests[request_id]["download_key"] is None:
        return {"error": "Download key not ready yet"}

    return requests[request_id]

@app.get("/download/{download_key}")
async def download_file(download_key: str, file: str | None = None):
    download_path = ROMS_FOLDER + download_key + "/"
    games = [f for f in os.listdir(download_path) if os.path.isfile(os.path.join(download_path, f))]
    if file:
        return FileResponse(download_path + file, filename=file)
    return FileResponse(download_path + games[0], filename=games[0])
