FROM python:3.11-slim as base

RUN apt-get update && apt-get install -y --no-install-recommends \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .



RUN chmod +x entrypoint.sh
ENTRYPOINT ["sh", "./entrypoint.sh"]