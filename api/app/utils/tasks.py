import os
import subprocess
from pathlib import Path
from datetime import datetime, timezone

from celery import Celery

from database.session import SessionLocal
from database.models import Download, DownloadStatusEnum

app = Celery("tasks", broker="pyamqp://guest@localhost//")

@app.task
def convert_to_chd(save_folder: str, download_folder: str, request_id: str, download_id: str):
    session = SessionLocal()

    session.add(Download(public_id=download_id, request_id=request_id, status=DownloadStatusEnum.PENDING, created_at=datetime.now(timezone.utc), updated_at=datetime.now(timezone.utc), expires_at=datetime.now(timezone.utc)))
    session.commit()

    os.makedirs(download_folder, exist_ok=True)

    subprocess.run(["./bin/create-chd-from-archives", save_folder, download_folder])
    subprocess.run(["rm", "-rf", save_folder])

    download_items = [f.relative_to(download_folder).as_posix() for f in Path(download_folder).rglob("*")]

    zip_filename = Path(download_folder).name + ".zip"
    subprocess.run(["zip", zip_filename, *download_items], cwd=download_folder)

    for item in Path(download_folder).iterdir():
        if item.name != zip_filename:
            if item.is_dir():
                subprocess.run(["rm", "-rf", str(item)])
            else:
                item.unlink()

    download = session.query(Download).filter_by(public_id=download_id).one_or_none()

    if download:
        download.status = DownloadStatusEnum.READY
        download.file_uri = os.path.abspath(os.path.join(download_folder, zip_filename))
        print(download.id)
        session.commit()
        session.close()