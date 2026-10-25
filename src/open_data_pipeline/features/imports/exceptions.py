from http import HTTPStatus

from open_data_pipeline.api.exceptions import AppException
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
IMPORT_SCHEMA_UPDATE_NOT_BASE_EXCEPTION = (
    "Import schema cannot be updated because it's not a base schema"
)
IMPORT_SCHEMA_ALREADY_UPDATED_EXCEPTION = "Import schema is already in the last version"


class InvalidFileException(AppException):
    status_code: HTTPStatus = HTTPStatus.BAD_REQUEST
    detail: str = INVALID_FILE_EXCEPTION


class InvalidFileHeadersException(AppException):
    status_code: HTTPStatus = HTTPStatus.BAD_REQUEST
    detail: str = INVALID_FILE_HEADERS_EXCEPTION


class InvalidFileDuplicatedHeaderException(AppException):
    status_code: HTTPStatus = HTTPStatus.BAD_REQUEST
    detail: str = INVALID_FILE_DUPLICATED_HEADER_EXCEPTION


class ImportNotFoundException(AppException):
    status_code: HTTPStatus = HTTPStatus.NOT_FOUND
    detail: str = IMPORT_NOT_FOUND_EXCEPTION


class ImportAlreadyProcessedException(AppException):
    status_code: HTTPStatus = HTTPStatus.CONFLICT
    detail: str = IMPORT_ALREADY_PROCESSED_EXCEPTION


class ImportFileNotFoundException(AppException):
    status_code: HTTPStatus = HTTPStatus.NOT_FOUND
    detail: str = IMPORT_FILE_NOT_FOUND_EXCEPTION


class ImportFileTooBigException(AppException):
    status_code: HTTPStatus = HTTPStatus.BAD_REQUEST
    detail: str = IMPORT_FILE_TOO_BIG_EXCEPTION


class ImportMissingSchemaException(AppException):
    status_code: HTTPStatus = HTTPStatus.BAD_REQUEST
    detail: str = IMPORT_MISSING_SCHEMA_EXCEPTION


class ImportSchemaHeadersMismatchException(AppException):
    status_code: HTTPStatus = HTTPStatus.CONFLICT
    detail: str = IMPORT_SCHEMA_HEADERS_MISMATCH


class ImportRowNotFoundException(AppException):
    status_code: HTTPStatus = HTTPStatus.NOT_FOUND
    detail: str = IMPORT_ROW_NOT_FOUND_EXCEPTION


class ImportRowFieldsMismatchSchemaException(AppException):
    status_code: HTTPStatus = HTTPStatus.BAD_REQUEST
    detail: str = IMPORT_ROW_FIELDS_MISMATCH_SCHEMA_EXCEPTION


class ImportRowValidationException(Exception):
    def __init__(self, errors: list[ImportRowError]) -> None:
        super().__init__()

        self.errors: list[ImportRowError] = errors


class ImportSchemaNotFoundException(AppException):
    status_code: HTTPStatus = HTTPStatus.NOT_FOUND
    detail: str = IMPORT_SCHEMA_NOT_FOUND


class ImportSchemaUpdateNotBaseException(AppException):
    status_code: HTTPStatus = HTTPStatus.CONFLICT
    detail: str = IMPORT_SCHEMA_UPDATE_NOT_BASE_EXCEPTION


class ImportSchemaAlreadyUpdatedException(AppException):
    status_code: HTTPStatus = HTTPStatus.CONFLICT
    detail: str = IMPORT_SCHEMA_ALREADY_UPDATED_EXCEPTION
