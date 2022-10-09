"""Main module for startup the whole backend."""
import fastapi
import uvicorn
from starlette.middleware.cors import CORSMiddleware

from backend import ioc
from backend.api import error_handlers
from backend.settings import base_settings

CONTAINER: ioc.IOCContainer = ioc.IOCContainer()


async def startup():
    """Do on start."""
    await CONTAINER.init_resources()

    # TODO - new modules wire here
    CONTAINER.wire(modules=[])


async def shutdown():
    """Do on end."""
    await CONTAINER.shutdown_resources()


APP_OBJ: fastapi.FastAPI = fastapi.FastAPI(
    on_startup=[startup],
    on_shutdown=[shutdown],
    docs_url=base_settings.doc_prefix,
    openapi_url=f"{base_settings.api_prefix}/openapi.json",
    openapi_tags=base_settings.tags_metadata,
    exception_handlers={
        fastapi.status.HTTP_500_INTERNAL_SERVER_ERROR: error_handlers.handle_error_500
    },
)

if base_settings.debug:
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
