"""Module with methods for handling errors on server."""

import fastapi
import pydantic
from fastapi import responses, status


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
