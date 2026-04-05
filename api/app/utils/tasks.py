import os
import subprocess
from pathlib import Path
from datetime import datetime, timezone

from celery import Celery

from config.database.session import SessionLocal
from config.database.models import Download

app = Celery("tasks", broker="pyamqp://guest@localhost//")

@app.task
def convert_to_chd(save_folder: str, download_folder: str, request_id: str, download_id: str):
    session = SessionLocal()

    session.add(Download(public_id=download_id, request_id=request_id, status="pending", created_at=datetime.now(timezone.utc), updated_at=datetime.now(timezone.utc), expires_at=datetime.now(timezone.utc)))
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

    download = session.query(Download).filter_by(public_id=download_id).one_or_none()

    if download:
        download.status = "ready"
        print(download.id)
        session.commit()
        session.close()