import csv
from collections.abc import Iterator
from pathlib import Path


def import_csv(file_path: Path) -> Iterator[dict[str, str]]:
    with open(file_path, "r", encoding="utf-8", newline="") as file:
        reader = csv.DictReader(file)

        yield from reader
