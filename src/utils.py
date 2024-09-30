from functools import lru_cache

from fastapi import HTTPException
from httpx import HTTPStatusError
from starlette.requests import Request
from starlette.status import HTTP_451_UNAVAILABLE_FOR_LEGAL_REASONS

from src.container import get_container
from src.database.redis.cache import Redis
from src.database.repository import ICacheRepository
from src.entities import IpEntity
from src.exceptions import CannotGetIpDataError, IpNotFromRussiaError
from src.ip.repository import IpRepository
from src.ip.validator import IPValidator


async def validate_request_country(request: Request) -> IpEntity:
    try:
        ip = await ICacheRepository(get_redis_database(), IpRepository()).get_ip_data(
            request.headers.get("X-Real-IP")
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


@lru_cache(1)
def get_redis_database() -> Redis:
    return get_container().resolve(Redis)
