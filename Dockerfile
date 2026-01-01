# ------------------------------------------------------
# Base image (match your runtime)
# ------------------------------------------------------
FROM python:3.13-slim

# ------------------------------------------------------
# Environment variables
# ------------------------------------------------------
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# ------------------------------------------------------
# Working directory
# ------------------------------------------------------
WORKDIR /app

# ------------------------------------------------------
# System dependencies (required for psycopg2, pgvector)
# ------------------------------------------------------
RUN apt-get update && apt-get install -y \
    build-essential \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# ------------------------------------------------------
# Install Python dependencies (cache-friendly)
# ------------------------------------------------------
COPY requirements.txt .

RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# ------------------------------------------------------
# Copy application source
# ------------------------------------------------------
COPY . .

# ------------------------------------------------------
# Expose FastAPI port
# ------------------------------------------------------
EXPOSE 8000

# ------------------------------------------------------
# Run FastAPI via uvicorn (CORRECT way)
# ------------------------------------------------------
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
