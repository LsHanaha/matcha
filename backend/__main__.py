"""Main module for startup the whole backend."""
import fastapi
import fastapi_jwt_auth.exceptions
import uvicorn
from starlette.middleware.cors import CORSMiddleware

from backend import ioc
from backend.api import error_handlers
from backend.auth import endpoints as auth_endpoints
from backend.settings import settings_base

CONTAINER: ioc.IOCContainer = ioc.IOCContainer()


async def startup():
    """Do on start."""
    await CONTAINER.init_resources()

    # TODO - new modules wire here
    CONTAINER.wire(modules=[auth_endpoints])


async def shutdown():
    """Do on end."""
    await CONTAINER.shutdown_resources()


APP_OBJ: fastapi.FastAPI = fastapi.FastAPI(
    on_startup=[startup],
    on_shutdown=[shutdown],
    docs_url=settings_base.doc_prefix,
    openapi_url=f"{settings_base.api_prefix}/openapi.json",
    openapi_tags=settings_base.tags_metadata,
    exception_handlers={
        fastapi.status.HTTP_500_INTERNAL_SERVER_ERROR: error_handlers.handle_error_500,
        fastapi_jwt_auth.exceptions.AuthJWTException: error_handlers.authjwt_exception_handler,
    },
)
APP_OBJ.include_router(auth_endpoints.ROUTER_OBJ, prefix="/auth", tags=["auth"])


if settings_base.debug:
    APP_OBJ.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


if __name__ == "__main__":
    uvicorn.run(
        "__main__:APP_OBJ",
        host="0.0.0.0",
        port=8888,
    )