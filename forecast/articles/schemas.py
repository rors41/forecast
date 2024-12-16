from datetime import datetime, timedelta
from pydantic import BaseModel, Field, field_validator
from pydantic_extra_types.coordinate import Latitude, Longitude

from forecast.articles.enums import ArticleLanguageEnum, ArticleStyleEnum


class StructuredOutputArticleSchema(BaseModel):
    article_body: str = Field(description="Body of the article", title="Article body")
    lead_paragraph: str = Field(
        description="Lead paragraph of the article", title="Lead paragraph"
    )
    title: str = Field(description="Title of the article", title="Title")


class DailyForecastDataRaw(BaseModel):
    temperature_2m_min: float
    temperature_2m_max: float
    apparent_temperature_min: float
    apparent_temperature_max: float
    precipitation_sum: float
    rain_sum: float
    showers_sum: float
    snowfall_sum: float
    precipitation_hours: float
    precipitation_probability_max: float
    weather_code: int
    sunrise: str
    sunset: str
    daylight_duration: float
    wind_speed_10m_max: float
    wind_gusts_10m_max: float
    wind_direction_10m_dominant: int
    uv_index_max: float
    uv_index_clear_sky_max: float


class DailyForecastData(BaseModel):
    temperature_2m_min: float
    temperature_2m_max: float
    apparent_temperature_min: float
    apparent_temperature_max: float
    precipitation_sum: float
    rain_sum: float
    showers_sum: float
    snowfall_sum: float
    precipitation_hours: float
    precipitation_probability_max: float
    weather_code: str
    sunrise: str
    sunset: str
    daylight_duration: str
    wind_speed_10m_max: float
    wind_gusts_10m_max: float
    wind_direction_10m_dominant: str
    uv_index_max: str
    uv_index_clear_sky_max: str


class CreateArticleRequest(BaseModel):
    language: ArticleLanguageEnum
    style: ArticleStyleEnum
    location: str = Field(examples=["Kosice"])
    date: str = Field(examples=["2024-12-16"])

    @field_validator("date", mode="before")
    @classmethod
    def validate_date(cls, value: str):
        try:
            parsed_date = datetime.strptime(value, "%Y-%m-%d")
        except ValueError:
            raise ValueError("Date must be in the format YYYY-MM-DD.")

        today = datetime.today()
        two_months_ago = today - timedelta(days=60)
        seven_days_ahead = today + timedelta(days=7)

        if not (two_months_ago <= parsed_date <= seven_days_ahead):
            raise ValueError(
                "Date must be at most 2 months in the past or 7 days in the future."
            )

        return value


class CreateArticleResponse(BaseModel):
    title: str
    lead_paragraph: str
    article_body: str
    latitude: Latitude
    longitude: Longitude


class LocationData(BaseModel):
    formatted: str
    latitude: Latitude
    longitude: Longitude
