ARG PYTHON_VERSION=3.12.7
FROM python:3.10-slim

# чтобы логи сразу выводились
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# системные зависимости (ffmpeg обязателен для аудио)
RUN apt-get update && apt-get install -y \
    ffmpeg \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# зависимости Python
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# копируем проект
COPY . .

# порт FastAPI
EXPOSE 8000

# запуск
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]