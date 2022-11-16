"""Module with methods for handling errors on server."""

import fastapi
import pydantic
from fastapi import responses, status
from fastapi_jwt_auth import exceptions


class BadResponse(pydantic.BaseModel):
    """Model for response with exceptions."""

    error: str


async def handle_error_500(
    _: fastapi.Request, exc: Exception
) -> responses.JSONResponse:
    """Handle 500 errors on server."""
    if isinstance(exc, fastapi.HTTPException):
        raise Exception
    return responses.JSONResponse(
        {"detail": BadResponse(error="Internal error.").dict()},
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    )


async def authjwt_exception_handler(
    _: fastapi.Request, exc: exceptions.AuthJWTException
) -> responses.JSONResponse:
    """Handle auth_jwt exceptions."""
    return responses.JSONResponse(
        status_code=exc.status_code, content={"detail": exc.message}
    )
