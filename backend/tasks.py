import os
import subprocess
from pathlib import Path
from datetime import datetime, timezone

from celery import Celery

from database import SessionLocal
from models import Download, Request
from utils import generate_public_id

app = Celery("tasks", broker="pyamqp://guest@localhost//")

@app.task
def convert_to_chd(save_folder: str, roms_folder: str, request_id: str):
    download_id = generate_public_id()
    download_folder = os.path.join(roms_folder, download_id)
    session = SessionLocal()

    print(f"{request_id=}, {download_id=}")

    request = session.query(Request).filter_by(public_id=request_id).one_or_none()

    if request == None:
        raise Exception("Request not found")

    request.status = "processing"

    session.add(Download(public_id=download_id, request_id=request.id, file_uri=download_folder, created_at=datetime.now(timezone.utc), expires_at=datetime.now(timezone.utc)))
    session.commit()

    os.makedirs(download_folder, exist_ok=True)
    subprocess.run(["./bin/create-chd-from-archives", save_folder, download_folder])
    subprocess.run(["rm", "-rf", save_folder])

    multi_disc_games_folder = os.path.join(download_folder, ".multi-disc-games")
    download_files = [f.relative_to(download_folder) for f in Path(download_folder).rglob("*") if f.is_file()]

    if os.path.exists(multi_disc_games_folder) and os.path.isdir(multi_disc_games_folder):
        subprocess.run(["zip", os.path.join(download_folder, Path(download_folder).name + ".zip"), *download_files], cwd=download_folder)

    m3u_files = [f for f in Path(download_folder).iterdir() if f.is_file() and f.suffix == ".m3u"]
    m3u_file = "" if len(m3u_files) == 0 else m3u_files[0]

    subprocess.run(["rm", "-rf", m3u_file, multi_disc_games_folder])

    request.status = "done"
    session.commit()
    session.close()