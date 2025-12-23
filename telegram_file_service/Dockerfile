FROM python:3.12-slim

WORKDIR /app

RUN apt-get update && apt-get install -y curl build-essential ffmpeg && pip install "poetry" && apt-get clean && rm -rf /var/lib/apt/lists/*
ENV PATH="/opt/poetry/bin:$PATH"


ENV POETRY_VIRTUALENVS_CREATE=false \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONPATH=/app/src

COPY pyproject.toml poetry.lock* /app/

RUN poetry config virtualenvs.create false
RUN poetry install --no-root

COPY src /app/src

EXPOSE 8000
