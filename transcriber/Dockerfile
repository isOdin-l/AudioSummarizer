# ============================================================
# Stage 1 — Base image with Poetry installed
# ============================================================
FROM python:3.13-slim AS base


RUN apt-get update && apt-get install -y curl build-essential ffmpeg && pip install "poetry" && apt-get clean && rm -rf /var/lib/apt/lists/*
ENV PATH="/opt/poetry/bin:$PATH"

WORKDIR /app

# ============================================================
# Stage 2 — Install dependencies
# ============================================================
FROM base AS builder

COPY pyproject.toml ./
COPY poetry.lock ./
COPY model/ ./model

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

CMD ["python", "main.py"]
