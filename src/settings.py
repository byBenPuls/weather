from pydantic_settings import BaseSettings


class RedisSettings(BaseSettings):
    REDIS_HOST: str
    REDIS_PORT: int
    REDIS_DB: int
    REDIS_PASSWORD: str


class OpenWeatherSettings(BaseSettings):
    OPENWEATHER_API_KEY: str


class IpSettings(BaseSettings):
    IP_API_KEY: str


class Settings(RedisSettings, OpenWeatherSettings, IpSettings):
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
