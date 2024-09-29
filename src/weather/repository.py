import datetime
from urllib.parse import urlencode

from src.container import get_container
from src.entities import Weather
from src.http.client import HttpClient
from src.weather.serializator import MeasurementResultOfWeatherSerializer


class WeatherRepository:
    def __init__(self):
        self.http_service: HttpClient = get_container().resolve(HttpClient)

    async def get_meteo(self, latitude: float, longitude: float) -> dict:
        current_time_params = [
            "temperature_2m",
            "relative_humidity_2m",
            "apparent_temperature",
            "is_day",
            "precipitation",
            "weather_code",
            "cloud_cover",
            "wind_speed_10m",
            "wind_direction_10m",
            "surface_pressure",
        ]
        daily_time_params = [
            "weather_code",
            "temperature_2m_max",
            "apparent_temperature_max",
            "precipitation_probability_max",
            "wind_speed_10m_max",
            "wind_direction_10m_dominant",
            "sunset",
            "sunrise",
        ]
        params = {
            "latitude": latitude,
            "longitude": longitude,
            "current": ",".join(current_time_params),
            "daily": ",".join(daily_time_params),
            "wind_speed_unit": "ms",
        }
        return await self.http_service.get(
            f"https://api.open-meteo.com/v1/forecast?{urlencode(params)}"
        )

    async def get_weather_data_by_coordinates(
        self, latitude: float, longitude: float
    ) -> tuple[Weather, list[Weather]]:
        json_data = await self.get_meteo(latitude, longitude)
        print(json_data)
        weekly_data = [
            MeasurementResultOfWeatherSerializer().get_serialized_data(
                json_data={
                    "time": datetime.datetime.strptime(date, "%Y-%m-%d"),
                    "temperature_2m": json_data["daily"]["temperature_2m_max"][i],
                    "apparent_temperature": json_data["daily"][
                        "apparent_temperature_max"
                    ][i],
                    "wind_speed_10m": json_data["daily"]["wind_speed_10m_max"][i],
                    "wind_direction_10m": json_data["daily"][
                        "wind_direction_10m_dominant"
                    ][i],
                    "precipitation": json_data["daily"][
                        "precipitation_probability_max"
                    ][i],
                    "weather_code": json_data["daily"]["weather_code"][i],
                }
            )
            for i, date in enumerate(json_data["daily"]["time"])
        ]
        current_data = MeasurementResultOfWeatherSerializer().get_serialized_data(
            json_data=json_data["current"]
        )
        return current_data, weekly_data
