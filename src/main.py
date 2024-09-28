from contextlib import asynccontextmanager
from typing import Annotated, AsyncIterator

from fastapi import FastAPI, Depends, HTTPException
from fastapi.responses import HTMLResponse
from httpx import HTTPStatusError
from starlette.requests import Request
from starlette.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from starlette.status import HTTP_451_UNAVAILABLE_FOR_LEGAL_REASONS

from src.database.redis.cache import Redis
from src.exceptions import CannotGetIpDataError, IpNotFromRussiaError
from src.ip.repository import IpRepository
from src.entities import IpEntity
from src.container import get_container
from src.ip.validator import IPValidator
from src.database.repository import ICacheRepository


def get_redis_database():
    return get_container().resolve(Redis)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    redis = get_redis_database()
    yield
    redis.close()


async def validate_request_country(request: Request) -> IpEntity | dict:
    print("work")
    try:
        ip = await ICacheRepository(get_redis_database(), IpRepository()).get_ip_data(
            request.client.host
        )
        validator = await IPValidator(ip).validate_ip_address()
        return validator
    except (CannotGetIpDataError, IpNotFromRussiaError, HTTPStatusError) as e:
        if isinstance(e, HTTPStatusError):
            return IpEntity(
                ip=request.client.host,
                hostname=request.client.host,
                city="Yekaterinburg",
                region="Sverdlovsk Oblast",
                country="RU",
                loc=(56.50485, 60.38511),
                org="unknown",
                postal="620000",
                timezone="Asia/Yekaterinburg",
            )
        raise HTTPException(status_code=HTTP_451_UNAVAILABLE_FOR_LEGAL_REASONS)


app = FastAPI(dependencies=[Depends(validate_request_country)], lifespan=lifespan)
app.mount("/src/pages/static", StaticFiles(directory="src/pages/static"), name="static")


@app.exception_handler(exc_class_or_status_code=HTTP_451_UNAVAILABLE_FOR_LEGAL_REASONS)
async def handle_451_http_error(request: Request, exc):
    return FileResponse(
        "src/pages/static/451.html", status_code=HTTP_451_UNAVAILABLE_FOR_LEGAL_REASONS
    )


@app.get("/")
async def root():
    return HTMLResponse()


@app.get("/weather", response_class=HTMLResponse)
async def say_hello(ip_data: Annotated[dict, Depends(validate_request_country)]):
    print(ip_data)
    return FileResponse("src/pages/static/main.html", media_type="text/html")
