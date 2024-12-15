FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim AS builder

WORKDIR /app
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-cache

FROM python:3.12.3-slim AS runtime

RUN useradd user -u 1000 --create-home && mkdir -p /app && chown -R user /app
USER user

WORKDIR /app
COPY --chown=user:user forecast /app/forecast
COPY --chown=user:user .env /app

COPY --from=builder /app/.venv /app/.venv

ENV PATH="/app/.venv/bin:$PATH"

CMD ["uvicorn", "forecast.main:app", "--host", "0.0.0.0", "--port", "8000"]
