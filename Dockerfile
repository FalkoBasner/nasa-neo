FROM python:3.12-slim AS builder

WORKDIR /app

RUN pip install uv

COPY pyproject.toml uv.lock ./
COPY src/ ./src/
RUN uv sync --no-dev --frozen


FROM python:3.12-slim

WORKDIR /app

COPY --from=builder /app/.venv ./.venv
COPY --from=builder /app/src ./src

EXPOSE 8000

CMD [".venv/bin/uvicorn", "nasa_neo.main:app", "--host", "0.0.0.0", "--port", "8000"]
