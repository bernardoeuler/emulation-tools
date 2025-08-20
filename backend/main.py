import os
import subprocess
import random
from pathlib import Path

from fastapi import FastAPI, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse

UPLOAD_DIR = str("/home/bernardo/Projects/learn/react-fastapi/user-uploads/")
DOWNLOAD_DIR = str("/home/bernardo/Projects/learn/react-fastapi/user-downloads/")
ROMS_DIR = DOWNLOAD_DIR + "roms/"

database = {
    "avaliable_downloads": [],
    "pending_downloads": [],
    "requests": [],
}

def generate_request_id():
    id = random.randint(10000000,99999999)

    while id in database["requests"]:
        id = random.randint(10000000,99999999)

    database["requests"].append(id)

    return str(id)

def generate_download_key():
    key = random.randint(10000000,99999999)

    while key in database["avaliable_downloads"]:
        key = random.randint(10000000,99999999)

    database["pending_downloads"].append(key)

    return str(key)

async def convert_file(file_uploads: list[UploadFile], request_id: str, download_key: str):
    save_dir = UPLOAD_DIR + request_id + "/"
    download_folder = ROMS_DIR + download_key

    subprocess.run(["mkdir", save_dir])

    for file_upload in file_uploads:
        data = await file_upload.read()
        if file_upload.filename:
            save_path = save_dir + file_upload.filename

            with open(save_path, "wb") as file:
                file.write(data)

    os.makedirs(ROMS_DIR, exist_ok=True)
    subprocess.run(["mkdir", download_folder])
    subprocess.run(["./bin/create-chd-from-archives", save_dir, download_folder])
    subprocess.run(["rm", "-rf", save_dir])

    multi_disc_games_folder = os.path.join(download_folder, ".multi-disc-games")
    download_files = [f.relative_to(download_folder) for f in Path(download_folder).rglob("*") if f.is_file()]

    if os.path.exists(multi_disc_games_folder) and os.path.isdir(multi_disc_games_folder):
        subprocess.run(["zip", os.path.join(download_folder, download_key + ".zip"), *download_files], cwd=download_folder)

    m3u_file = [f for f in Path(download_folder).iterdir() if f.is_file() and f.suffix == ".m3u"][0]

    subprocess.run(["rm", "-rf", m3u_file, multi_disc_games_folder])

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/uploadfile/")
async def create_upload_file(file_uploads: list[UploadFile]):
    request_id = generate_request_id()
    download_key = generate_download_key()

    os.makedirs(UPLOAD_DIR, exist_ok=True)

    await convert_file(file_uploads, request_id, download_key)

    return {"request_id": request_id}

@app.get("/download/{download_key}")
async def download_file(download_key: str, file: str | None = None):
    download_path = ROMS_DIR + download_key + "/"
    games = [f for f in os.listdir(download_path) if os.path.isfile(os.path.join(download_path, f))]
    if file:
        return FileResponse(download_path + file, filename=file)
    return FileResponse(download_path + games[0], filename=games[0])
