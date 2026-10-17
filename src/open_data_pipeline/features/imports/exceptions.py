from open_data_pipeline.features.imports.csv_reader import CSV_MAX_ROWS_SIZE

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


class InvalidFileException(Exception): ...


class InvalidFileHeadersException(Exception): ...


class InvalidFileDuplicatedHeaderException(Exception): ...


class ImportNotFoundException(Exception): ...


class ImportAlreadyProcessedException(Exception): ...


class ImportFileNotFoundException(Exception): ...


class ImportFileTooBigException(Exception): ...


class ImportMissingSchemaException(Exception): ...


class ImportSchemaHeadersMismatchException(Exception): ...
