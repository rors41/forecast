from typing import Annotated

from fastapi import APIRouter, Depends
from httpx import AsyncClient
from langchain_openai import ChatOpenAI

from forecast.articles.llm import create_weather_forecast_article
from forecast.articles.schemas import (
    CreateArticleRequest,
    CreateArticleResponse,
)
from forecast.articles.service import geocode_location, weather_forecast_data
from forecast.auth import verify_bearer_token
from forecast.dependency import get_httpx_client, get_llm

articles_router = APIRouter(prefix="/articles", tags=["articles"])


@articles_router.post("/")
async def create_article(
    _: Annotated[None, Depends(verify_bearer_token)],
    httpx_client: Annotated[AsyncClient, Depends(get_httpx_client)],
    llm: Annotated[ChatOpenAI, Depends(get_llm)],
    body: CreateArticleRequest,
) -> CreateArticleResponse:
    """
    **Request body**
    - language - language of the generated article
    - style - article style
    - location - location of weather forecast article, should be a name of a city/village
    - date - date of weather forecast, must be in YYYY-MM-DD format and in following interval 60 days in past <= date <= 7 days in future
    """
    location_data = await geocode_location(httpx_client, body.location)
    weather_data = await weather_forecast_data(httpx_client, body.date, location_data)
    article = await create_weather_forecast_article(
        llm=llm,
        article_style=body.style,
        article_language=body.language,
        date=body.date,
        location_data=location_data,
        weather_data=weather_data,
    )
    return CreateArticleResponse(
        title=article.title,
        lead_paragraph=article.lead_paragraph,
        article_body=article.article_body,
        latitude=location_data.latitude,
        longitude=location_data.longitude,
    )
