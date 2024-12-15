from datetime import datetime
from fastapi import HTTPException, status
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

from forecast.articles.enums import (
    ARTICLE_STYLE_MAP,
    ArticleLanguageEnum,
    ArticleStyleEnum,
)
from forecast.articles.schemas import (
    DailyForecastData,
    LocationData,
    StructuredOutputArticleSchema,
)


ARTICLE_PROMPT_TEMPLATE = ChatPromptTemplate(
    [
        (
            "system",
            """\
You are a highly skilled and creative weather forecast writer. The user will provide you with the latest forecast data, and your task is to craft an engaging and accurate weather forecast based on this information.

Instructions:
    1. {article_style}
    2. The article must be written in {article_language} language.
    3. Start with article body, then create lead paragraph and finish with the title of the article.
    4. Make sure to mention day of the week and the date
        """,
        ),
        (
            "user",
            """\
Here are is the forecast data:
Location: {location}
Current day of the week = {weekday}
Forecast is made for date = {date}
Minimum daily air temperature at 2 meters above ground = {temperature_2m_min}°C
Maximum daily air temperature at 2 meters above ground = {temperature_2m_max}°C
Minimum daily apparent temperature = {apparent_temperature_min}°C
Maximum and daily apparent temperature = {apparent_temperature_max}°C
Sum of daily precipitation (including rain, showers and snowfall) = {precipitation_sum}mm
Sum of daily rain = {rain_sum}mm
Sum of daily showers = {showers_sum}mm
Sum of daily snowfall = {snowfall_sum}cm
The number of hours with rain = {precipitation_hours}hours
Probability of precipitation = {precipitation_probability_max}%
The most severe weather condition on a given day = {weather_code}
Sun rise time = {sunrise}
Sun set time = {sunset}
Amount of daylight per day = {daylight_duration}
Maximum wind speed and gusts on a day = {wind_speed_10m_max}km/h
Maximum wind speed and gusts on a day = {wind_gusts_10m_max}km/h
Dominant wind direction = {wind_direction_10m_dominant}
Daily maximum in UV Index = {uv_index_max}
Daily maximum in UV Index when sky is clear = {uv_index_clear_sky_max}
        """,
        ),
    ]
)


async def create_weather_forecast_article(
    llm: ChatOpenAI,
    article_style: ArticleStyleEnum,
    article_language: ArticleLanguageEnum,
    date: str,
    location_data: LocationData,
    weather_data: DailyForecastData,
) -> StructuredOutputArticleSchema:
    structured_llm = llm.with_structured_output(StructuredOutputArticleSchema)
    chain = ARTICLE_PROMPT_TEMPLATE | structured_llm
    # setup retry when this fails
    response = await chain.ainvoke(
        input={
            "date": date,
            "weekday": datetime.fromisoformat(date).strftime("%A"),
            "article_style": ARTICLE_STYLE_MAP[article_style],
            "article_language": article_language.value,
            "location": location_data.formatted,
            **weather_data.model_dump(),
        }
    )

    if not isinstance(response, StructuredOutputArticleSchema):
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return response
