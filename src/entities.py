from dataclasses import dataclass, is_dataclass
from datetime import datetime


def nested_dataclass(*args, **kwargs):
    def wrapper(cls):
        cls = dataclass(cls, **kwargs)
        original_init = cls.__init__

        def __init__(self, *args, **kwargs):
            for name, value in kwargs.items():
                field_type = cls.__annotations__.get(name, None)
                if is_dataclass(field_type) and isinstance(value, dict):
                    new_obj = field_type(**value)
                    kwargs[name] = new_obj
            original_init(self, *args, **kwargs)

        cls.__init__ = __init__
        return cls

    return wrapper(args[0]) if args else wrapper


@dataclass
class IpEntity:
    ip: str
    hostname: str
    city: str
    region: str
    country: str
    loc: tuple
    org: str
    postal: str
    timezone: str


@dataclass(frozen=True)
class Weather:
    time: datetime
    temperature: float  # in degrees of Celsius
    relative_humidity: float  # in percents
    weather_code: int
    precipitation: float  # in percents
    wind_speed: float  # in m/s
    wind_direction: str  # in directions on russian

    surface_pressure: float | None = None  # in hPa
    feels_like: float | None = None  # in degrees of Celsius
    is_day: bool | None = None


@nested_dataclass
class DailyAndWeeklyWeather:
    daily: Weather
    weekly: list[Weather]
