# syntax=docker/dockerfile:1

FROM python:3.11-slim AS base

# Prevents Python from writing pyc files and buffering stdout/stderr
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# System deps
RUN apt-get update \
 && apt-get install -y --no-install-recommends build-essential \
 && rm -rf /var/lib/apt/lists/*

# Install Python deps first for better layer caching
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

# Copy application code
COPY . /app

EXPOSE 8000

ENV FLASK_ENV=production \
    FLASK_DEBUG=False

# Run Uvicorn with the ASGI-wrapped Flask app
CMD ["uvicorn", "app:asgi_app", "--host", "0.0.0.0", "--port", "8000", "--workers", "2"]
