from fastapi import Request
from httpx import AsyncClient
from langchain_openai import ChatOpenAI

from forecast.config import CONFIG


async def get_httpx_client(request: Request) -> AsyncClient:
    return request.state.httpx_client  # pyright: ignore[reportAny]


async def get_llm() -> ChatOpenAI:
    return ChatOpenAI(model=CONFIG.openai_model, api_key=CONFIG.openai_api_key)
