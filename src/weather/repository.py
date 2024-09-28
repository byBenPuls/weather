from urllib.parse import urlencode

from src.container import get_container
from src.http.client import HttpClient
from src.settings import settings


class WeatherRepository:
    def __init__(self):
        self.http_service: HttpClient = get_container().resolve(HttpClient)

    async def get_weather_data_from_city(
        self, city: str, country_iso_code: str
    ) -> dict:
        params = {
            "q": f"{city},{country_iso_code.upper()}",
            "appid": settings.WEATHER_API_KEY,
        }
        return await self.http_service.get(
            f"https://api.openweathermap.org/data/2.5/weather?{urlencode(params)}"
        )
