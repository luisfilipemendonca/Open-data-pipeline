from pathlib import Path

from open_data_pipeline.features.imports.csv_reader import import_csv


def test_import_csv(tmp_path: Path):
    csv_file = tmp_path / "valid.csv"
    csv_file.write_text(
        "id,first_name,last_name,email,age,city,salary,joined\n"
        "1,John,Doe,john.doe@example.com,25,New York,100000,2021-01-01\n"
        "2,John,Doe,john.doe@example.com,25,New York,100000,2021-01-01\n",
        encoding="utf-8",
    )

    result = list(import_csv(csv_file))

    assert len(result) == 2
    assert result[0]["first_name"] == "John"


def test_import_csv_empty(tmp_path: Path):
    csv_file = tmp_path / "empty.csv"
    csv_file.write_text(
        "id,first_name,last_name,email,age,city,salary,joined", encoding="utf-8"
    )

    result = list(import_csv(csv_file))

    assert len(result) == 0


def test_import_csv_fields_as_strings(tmp_path: Path):
    csv_file = tmp_path / "fields_as_strings.csv"
    csv_file.write_text(
        "id,first_name,last_name,email,age,city,salary,joined\n"
        "1,John,Doe,john.doe@example.com,25,New York,100000,2021-01-01\n",
        encoding="utf-8",
    )

    result = list(import_csv(csv_file))

    assert isinstance(result[0]["id"], str)
    assert isinstance(result[0]["age"], str)
    assert result[0]["id"] == "1"
    assert result[0]["age"] == "25"
