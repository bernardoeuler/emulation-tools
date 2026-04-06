import os
import subprocess
import uuid
from pathlib import Path
from datetime import datetime, timedelta, timezone

from celery import Celery

from database.session import SessionLocal
from database.models import Download, Request, DownloadStatusEnum, RequestStatusEnum

DOWNLOAD_FOLDER = Path(os.getenv("DOWNLOAD_FOLDER", "downloads"))

app = Celery("tasks", broker="pyamqp://guest@localhost//")

@app.task
def convert_to_chd(save_folder: str, request_id: str):
    download_id = uuid.uuid4().hex
    download_folder = DOWNLOAD_FOLDER / download_id
    session = SessionLocal()

    request = session.query(Request).filter_by(public_id=request_id).one_or_none()

    if not request:
        session.close()
        return

    download = Download(public_id=download_id, request_id=request.id, status=DownloadStatusEnum.PENDING, created_at=datetime.now(timezone.utc), updated_at=datetime.now(timezone.utc), expires_at=datetime.now(timezone.utc) + timedelta(hours=1))
    request.status = RequestStatusEnum.IN_PROGRESS
    
    session.add(download)

    try:
        session.commit()

        DOWNLOAD_FOLDER.mkdir(parents=True, exist_ok=True)

        subprocess.run(["./bin/create-chd-from-archives", save_folder, str(download_folder), "-q"], check=True)
        subprocess.run(["rm", "-rf", save_folder])

        download_items = [f.relative_to(download_folder).as_posix() for f in Path(download_folder).rglob("*")]
        zip_filename = f"{Path(download_folder).name}.zip"

        subprocess.run(["zip", zip_filename, *download_items], cwd=str(download_folder), check=True)

        for item in Path(download_folder).iterdir():
            if item.name != zip_filename:
                if item.is_dir():
                    subprocess.run(["rm", "-rf", str(item)])
                else:
                    item.unlink()

        download.status = DownloadStatusEnum.READY
        download.file_uri = (download_folder / zip_filename).resolve().as_uri()

        request.status = RequestStatusEnum.DONE

        session.commit()
    except Exception:
        download.status = DownloadStatusEnum.FAILED
        request.status = RequestStatusEnum.FAILED

        session.commit()
    finally:
        session.close()
