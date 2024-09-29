from src.weather.serializator import WindDirectionSerializer


def test_wind_serialization():
    serializer = WindDirectionSerializer().convert_degrees_to_cardinal(216)
    assert serializer == "ЮЗ"
