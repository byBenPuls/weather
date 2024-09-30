import datetime
from typing import Annotated

from fastapi import Depends, APIRouter
from starlette.requests import Request

from src.constants import WEATHER_IMAGES, SHORT_RUSSIAN_WEEKDAYS
from src.database.repository import ICacheRepository
from src.entities import IpEntity
from src.pages import templates
from src.utils import get_redis_database, validate_request_country
from src.weather.repository import WeatherRepository

router = APIRouter()


@router.get("/")
async def root(
    request: Request, ip_data: Annotated[IpEntity, Depends(validate_request_country)]
):
    lat, lon = (56.8519, 60.6122)
    weather_data = await ICacheRepository(
        get_redis_database(), WeatherRepository()
    ).get_weather_data_by_coordinates(lat, lon)
    print(weather_data)
    current_weather = weather_data.daily
    location = ip_data.city
    temperature = weather_data.daily.temperature
    wind_speed = weather_data.daily.wind_speed
    wind_direction = weather_data.daily.wind_direction

    weather_condition = "Sunny"
    weather_icon = WEATHER_IMAGES[str(current_weather.weather_code)][
        "day" if current_weather.is_day else "night"
    ]

    weekly_weather = [
        *(
            {
                "date": SHORT_RUSSIAN_WEEKDAYS[day.time.strftime("%A")]
                if day.time.date() != datetime.datetime.now().date()
                else "Сегодня",
                "temperature": day.temperature,
                "weather_icon": WEATHER_IMAGES[str(day.weather_code)]["day"]["image"],
                "description": WEATHER_IMAGES[str(day.weather_code)]["day"][
                    "description"
                ],
            }
            for day in weather_data.weekly
        )
    ]

    return templates.TemplateResponse(
        name="main.html",
        request=request,
        context={
            "location": location,
            "coords": f"({ip_data.loc[0]}, {ip_data.loc[1]})",
            "temperature": temperature,
            "description": weather_icon["description"],
            "precipitation": int(current_weather.precipitation),
            "surface_pressure": int(current_weather.surface_pressure),
            "feels_like": current_weather.feels_like,
            "wind_speed": wind_speed,
            "wind_direction": wind_direction,
            "relative_humidity": current_weather.relative_humidity,
            "weather_condition": weather_condition,
            "weather_icon": weather_icon["image"],
            "weekly_weather": weekly_weather,
        },
    )
