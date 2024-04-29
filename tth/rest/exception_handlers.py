import logging
from http import HTTPStatus

from asyncpg.exceptions import UndefinedTableError
from fastapi import HTTPException
from fastapi.requests import Request
from fastapi.responses import JSONResponse
from sqlalchemy.exc import DBAPIError

from tth.common.exceptions import (
    HackTemplateException,
    UserWithUsernameAlreadyExistsException,
)
from tth.rest.models import StatusResponse

log = logging.getLogger(__name__)


async def http_exception_handler(request: Request, exc: HTTPException) -> JSONResponse:
    return _exception_json_response(status_code=exc.status_code, message=exc.detail)


def user_already_exists_handler(
    request: Request,
    exc: UserWithUsernameAlreadyExistsException,
) -> JSONResponse:
    return _exception_json_response(
        status_code=HTTPStatus.BAD_REQUEST,
        message=exc.message,
    )


def internal_server_error_handler(
    request: Request, exc: HackTemplateException
) -> JSONResponse:
    return _exception_json_response(
        status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
        message="Unknown internal server error",
    )


def db_api_error_handler(request: Request, exc: DBAPIError) -> JSONResponse:
    original_source = exc.__cause__.__cause__  # type: ignore[union-attr]
    if isinstance(original_source, UndefinedTableError):
        log.warning(
            "Table was not found: %s. Maybe you forgot to create it?",
            original_source,
        )
    else:
        log.warning("Occured DB API error: %s", exc)
    return _exception_json_response(
        status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
        message="Unknown internal server error",
    )


def _exception_json_response(status_code: int, message: str) -> JSONResponse:
    return JSONResponse(
        status_code=status_code,
        content=StatusResponse(message=message).model_dump(),
    )
