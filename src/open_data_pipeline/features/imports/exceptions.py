from open_data_pipeline.features.imports.csv_reader import CSV_MAX_ROWS_SIZE
from open_data_pipeline.features.imports.schemas import ImportRowError

INVALID_FILE_EXCEPTION = "Invalid file extension"
INVALID_FILE_HEADERS_EXCEPTION = "Invalid file headers"
INVALID_FILE_DUPLICATED_HEADER_EXCEPTION = "Invalid file duplicated header"
IMPORT_NOT_FOUND_EXCEPTION = "Import not found"
IMPORT_ALREADY_PROCESSED_EXCEPTION = "Import already processed"
IMPORT_FILE_NOT_FOUND_EXCEPTION = "Import file not found"
IMPORT_FILE_TOO_BIG_EXCEPTION = (
    f"Import file needs to have under {CSV_MAX_ROWS_SIZE} rows"
)
IMPORT_MISSING_SCHEMA_EXCEPTION = "Missing schema in import"
IMPORT_SCHEMA_HEADERS_MISMATCH = "Schema fields don't match file headers"
IMPORT_ROW_NOT_FOUND_EXCEPTION = "Import row not found"
IMPORT_ROW_FIELDS_MISMATCH_SCHEMA_EXCEPTION = "Import row fields mismatch the schema"
IMPORT_SCHEMA_NOT_FOUND = "Import schema not found"


class InvalidFileException(Exception): ...


class InvalidFileHeadersException(Exception): ...


class InvalidFileDuplicatedHeaderException(Exception): ...


class ImportNotFoundException(Exception): ...


class ImportAlreadyProcessedException(Exception): ...


class ImportFileNotFoundException(Exception): ...


class ImportFileTooBigException(Exception): ...


class ImportMissingSchemaException(Exception): ...


class ImportSchemaHeadersMismatchException(Exception): ...


class ImportRowNotFoundException(Exception): ...


class ImportRowFieldsMismatchSchemaException(Exception): ...


class ImportRowValidationException(Exception):
    def __init__(self, errors: list[ImportRowError]) -> None:
        super().__init__()

        self.errors: list[ImportRowError] = errors


class ImportSchemaNotFoundException(Exception): ...
