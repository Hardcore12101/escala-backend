FROM python:3.13-slim

WORKDIR /app

# Dependências do sistema
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Dependências Python
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# Código
COPY . .

ENV PYTHONPATH=/app/src

# Start: roda migrations e sobe a API
CMD ["sh", "-c", "echo 'ANTES ALEMBIC' && alembic upgrade head && echo 'ANTES UVICORN' && exec uvicorn app.main:app --host 0.0.0.0 --port $PORT"]

