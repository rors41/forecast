from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Config(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")  # pyright: ignore[reportUnannotatedClassAttribute]

    openai_api_key: SecretStr
    openai_model: str = "gpt-4o"

    forecast_api_url: str = "https://api.open-meteo.com/v1/forecast"

    geoapify_geocode_api_url: str = "https://api.geoapify.com/v1/geocode/search"
    geoapify_api_key: SecretStr

    app_api_key: SecretStr


CONFIG = Config()  # pyright: ignore[reportCallIssue]
