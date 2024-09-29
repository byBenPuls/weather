import pytest
from src.weather.repository import WeatherRepository

pytest_plugins = ("pytest_asyncio",)


@pytest.mark.asyncio
async def test_weather_serializer():
    data = await WeatherRepository().get_weather_data_by_coordinates(56.8519, 60.6122)

    print(data)
