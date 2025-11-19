# ============================================================
# Stage 1 — Base image with Poetry installed
# ============================================================
FROM python:3.13-slim AS base

ENV POETRY_HOME="/opt/poetry"
ENV PATH="$POETRY_HOME/bin:$PATH"

RUN apt-get update && apt-get install -y curl build-essential && curl -sSL https://install.python-poetry.org | python3 - && apt-get clean && rm -rf /var/lib/apt/lists/*

WORKDIR /app


# ============================================================
# Stage 2 — Install dependencies
# ============================================================
FROM base AS builder

COPY pyproject.toml ./
COPY poetry.lock ./

RUN poetry config virtualenvs.create false
RUN poetry install --no-root


# ============================================================
# Stage 3 — Runtime (only required dependencies)
# ============================================================
FROM python:3.13-slim AS runtime

ENV PYTHONUNBUFFERED=1 PYTHONDONTWRITEBYTECODE=1 PYTHONPYCACHEPREFIX="/app/.pycache"

WORKDIR /app

# Copy installed packages from builder
COPY --from=builder /usr/local /usr/local

# Copy app source
COPY . .

CMD ["python", "-m", "fastapi", "run", "main.py"]
