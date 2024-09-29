from src.entities import Weather


class WindDirectionSerializer:
    def convert_degrees_to_cardinal(self, degrees: int) -> str:
        # source:
        # https://uni.edu/storm/Wind%20Direction%20slide.pdf
        match degrees:
            case _ if 350 < degrees < 360 or degrees < 10:
                return "С"
            case _ if 10 < degrees < 70:
                return "СВ"
            case _ if 70 < degrees < 100:
                return "В"
            case _ if 100 < degrees < 160:
                return "ЮВ"
            case _ if 160 < degrees < 190:
                return "Ю"
            case _ if 190 < degrees < 250:
                return "ЮЗ"
            case _ if 250 < degrees < 280:
                return "З"
            case _ if 280 < degrees < 350:
                return "СЗ"


class PressureSerializer:
    def convert_hecto_pascals_to_mm_hg(self, hecto_pascals: float) -> float:
        # source:
        # https://www.gradusniki.ru/help/mm-hpa.pdf
        return hecto_pascals / 1.333


class MeasurementResultOfWeatherSerializer(WindDirectionSerializer, PressureSerializer):
    def get_serialized_data(self, json_data: dict) -> Weather:
        return Weather(
            time=json_data.get("time"),
            temperature=json_data.get("temperature_2m"),
            feels_like=json_data.get("apparent_temperature"),
            relative_humidity=json_data.get("relative_humidity_2m"),
            weather_code=json_data.get("weather_code"),
            surface_pressure=self.convert_hecto_pascals_to_mm_hg(
                json_data.get("surface_pressure")
            )
            if json_data.get("surface_pressure")
            else None,
            precipitation=json_data.get("precipitation"),
            wind_speed=json_data.get("wind_speed_10m"),
            wind_direction=self.convert_degrees_to_cardinal(
                json_data.get("wind_direction_10m")
            ),
            is_day=json_data.get("is_day"),
        )
