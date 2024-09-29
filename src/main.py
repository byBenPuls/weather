from contextlib import asynccontextmanager
from typing import AsyncIterator

from fastapi import FastAPI, Depends
from fastapi.responses import FileResponse
from starlette.requests import Request
from starlette.staticfiles import StaticFiles
from starlette.status import HTTP_451_UNAVAILABLE_FOR_LEGAL_REASONS

from src.pages import router
from src.pages.index import router as index_router
from src.utils import get_redis_database, validate_request_country


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    redis = get_redis_database()
    yield
    await redis.close_connection()


app = FastAPI(dependencies=[Depends(validate_request_country)], lifespan=lifespan)
app.mount("/src/pages/static", StaticFiles(directory="src/pages/static"), name='static')

app.include_router(router)
app.include_router(index_router)


@app.exception_handler(exc_class_or_status_code=HTTP_451_UNAVAILABLE_FOR_LEGAL_REASONS)
async def handle_451_http_error(request: Request, exc):
    return FileResponse(
        "src/pages/static/451.html", status_code=HTTP_451_UNAVAILABLE_FOR_LEGAL_REASONS
    )
