from io import BytesIO

from fastapi import UploadFile

from open_data_pipeline.features.imports.file_validator import validate_file


def test_validate_file_valid():
    assert validate_file(UploadFile(filename="test.csv", file=BytesIO(b"test")))


def test_validate_file_invalid():
    assert not validate_file(UploadFile(filename="test.txt", file=BytesIO(b"test")))


def test_validate_file_uppercase_extension():
    assert validate_file(UploadFile(filename="test.CSV", file=BytesIO(b"test")))


def test_validate_file_no_extension():
    assert not validate_file(UploadFile(filename="test", file=BytesIO(b"test")))


def test_validate_file_no_filename():
    assert not validate_file(UploadFile(file=BytesIO(b"test")))
