from pathlib import Path

from fastapi import UploadFile


def validate_file(file: UploadFile) -> bool:
    if not file.filename:
        return False

    return Path(file.filename.lower()).suffix == ".csv"
