# Backend API Dockerfile
FROM python:3.13-slim

WORKDIR /app

# Install system dependencies including build dependencies for psycopg2
RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    libpq-dev \
    python3-dev \
    libavif-dev \
    libnss3 \
    libatk1.0-0 \
    libatk-bridge2.0-0 \
    libcups2 \
    libdrm2 \
    libxkbcommon0 \
    libxcomposite1 \
    libxdamage1 \
    libxfixes3 \
    libxrandr2 \
    libgbm1 \
    libasound2 \
    libpangocairo-1.0-0 \
    libgtk-3-0 \
    ca-certificates \
    fonts-liberation \
    && rm -rf /var/lib/apt/lists/*

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

# Copy all files (needed for editable install)
COPY . .

ENV UV_PROJECT_ENVIRONMENT=system

# Install dependencies using uv
RUN uv pip install --system --no-cache .

# Expose port
EXPOSE 8000