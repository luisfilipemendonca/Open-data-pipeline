import csv
import shutil
from collections.abc import Iterator
from pathlib import Path
from uuid import uuid4

from fastapi import UploadFile


def import_csv(file_path: Path) -> Iterator[dict[str, str]]:
    with open(file_path, "r", encoding="utf-8", newline="") as file:
        reader = csv.DictReader(file)

        yield from reader


def read_csv_headers(file_path: Path) -> list[str]:
    with open(file_path, "r", encoding="utf-8", newline="") as file:
        reader = csv.DictReader(file)
        return [name for name in (reader.fieldnames or [])]


TEMP_FILES_DIR = Path("tmp/imports")


def save_upload_file(file: UploadFile) -> tuple[str, Path]:
    TEMP_FILES_DIR.mkdir(parents=True, exist_ok=True)
    file_key = f"{uuid4()}.csv"
    file_path = TEMP_FILES_DIR / file_key

    try:
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
    except OSError:
        file_path.unlink(missing_ok=True)
        raise

    return file_key, file_path
