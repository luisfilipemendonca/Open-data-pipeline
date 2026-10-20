from http import HTTPStatus

from open_data_pipeline.api.exceptions import AppException

NOT_FOUND_SCHEMA_EXCEPTION = "Schema not found."


class NotFoundSchemaException(AppException):
    status_code = HTTPStatus.NOT_FOUND
    detail = NOT_FOUND_SCHEMA_EXCEPTION
