from dataclasses import dataclass, asdict
from src.database.redis.cache import Redis
from src.entities import IpEntity, DailyAndWeeklyWeather, Weather
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
            return IpEntity(**cache_data)
        data = await self.repository.get_entity(ip)
        await self.cache.record_in_cache(
            self._key_builder(ip), asdict(data), 60 * 60 * 24 * 7
        )
        return data

    async def get_weather_data_by_coordinates(
        self, latitude: float, longitude: float
    ) -> DailyAndWeeklyWeather | None:
        coordinates = f"{latitude},{longitude}"
        if cache_data := await self.cache.get_from_cache(
            key=self._key_builder(coordinates)
        ):
            return DailyAndWeeklyWeather(
                daily=Weather(**cache_data["daily"]),
                weekly=[Weather(**day) for day in cache_data["weekly"]],
            )
        daily, weekly = await self.repository.get_weather_data_by_coordinates(
            latitude, longitude
        )
        weather = DailyAndWeeklyWeather(daily=daily, weekly=weekly)
        await self.cache.record_in_cache(
            self._key_builder(coordinates), asdict(weather), 900
        )
        return weather
