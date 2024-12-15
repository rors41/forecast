from contextlib import asynccontextmanager

import httpx
from fastapi import FastAPI

from forecast.articles.router import articles_router


@asynccontextmanager
async def lifespan(_: FastAPI):
    async with httpx.AsyncClient(timeout=30) as client:
        yield {"httpx_client": client}


app = FastAPI(lifespan=lifespan)

app.include_router(articles_router)
