from dataclasses import dataclass, asdict
from src.database.redis.cache import Redis
from src.entities import IpEntity
from src.weather.repository import WeatherRepository
from src.ip.repository import IpRepository


@dataclass
class ICacheRepository(IpRepository, WeatherRepository):
    cache: Redis

    repository: IpRepository | WeatherRepository

    def _key_builder(self, key: str) -> str:
        return f"v1:{key}"

    async def get_ip_data(self, ip: str) -> IpEntity | None:
        if cache_data := await self.cache.get_from_cache(key=self._key_builder(ip)):
            return cache_data
        data = await self.repository.get_entity(ip)
        await self.cache.record_in_cache(self._key_builder(ip), asdict(data))
        return data

    async def get_weather_data_from_city(
        self, city: str, country_iso_code: str
    ) -> dict | None:
        return await self.cache.get_from_cache(self._key_builder(city))
