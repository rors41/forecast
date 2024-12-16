# Installation
- download uv [https://github.com/astral-sh/uv](https://github.com/astral-sh/uv)
- rename `.env.example` to `.env` and set api keys
- run `uv sync --frozen` to install dependencies
- run `uv run fastapi dev forecast/main.py` to start the fastapi server
