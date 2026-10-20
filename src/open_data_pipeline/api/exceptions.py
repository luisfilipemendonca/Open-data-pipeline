from http import HTTPStatus

from fastapi import Request
from fastapi.responses import JSONResponse


class AppException(Exception):
    status_code = HTTPStatus.INTERNAL_SERVER_ERROR
    detail = "Internal server error"


def app_exception_handler(_: Request, exception: Exception) -> JSONResponse:
    if not isinstance(exception, AppException):
        raise exception

    return JSONResponse(
        status_code=exception.status_code, content={"detail": exception.detail}
    )
