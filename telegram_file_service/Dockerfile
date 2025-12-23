FROM python:3.12-slim

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
  && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir poetry

ENV POETRY_VIRTUALENVS_CREATE=false \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONPATH=/app/src

COPY pyproject.toml poetry.lock* /app/
RUN poetry install --no-interaction --no-ansi

COPY src /app/src

EXPOSE 8000
