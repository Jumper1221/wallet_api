# Wallet REST API

Микросервис для управления кошельками с поддержкой операций пополнения и снятия средств.

## 📋 Содержание

- [Стек технологий](#-стек-технологий)
- [Запуск проекта](#-запуск-проекта)
- [API Endpoints](#-api-endpoints)
- [Тестирование](#-тестирование)
- [Особенности реализации](#-особенности-реализации)
- [Миграции](#-миграции)
- [Переменные окружения](#-переменные-окружения)

## 🛠 Стек технологий

- Python 3.11
- Django 4.2
- Django REST Framework
- PostgreSQL 16
- Docker + Docker Compose

## 🚀 Запуск проекта

### Требования:

- Docker 20.10+
- Docker Compose 2.20+

1. Клонировать репозиторий:

```bash
git clone https://github.com/Jumper1221/wallet_api
cd wallet-api
```

2. Запустить сервисы:

```bash
docker-compose up --build
```

Сервисы будут доступны:

API: http://localhost:8000

PGAdmin: http://localhost:8080

PostgreSQL: порт 5432

## 📡 API Endpoints

### Получить баланс кошелька

```
GET /api/v1/wallets/{uuid}/
```

Пример ответа:

```json
{
  "balance": "1500.00"
}
```

### Выполнить операцию

```
POST /api/v1/wallets/{uuid}/operation/
```

Тело запроса:

```json
{
  "operation_type": "WITHDRAW",
  "amount": "500.00"
}
```

Пример ответа:

```json
{
  "balance": 200.0
}
```

## 🧪 Тестирование

### Запуск тестов:

```bash
docker-compose exec wallet_app python manage.py test
```

Тесты покрывают:

- Основные сценарии операций
- Конкурентные запросы (5+ параллельных транзакций)
- Валидацию данных

## 🔐 Особенности реализации

### Безопасность транзакций

- **Атомарные операции**: Использование ```select_for_update``` и F-выражений для предотвращения race condition

- **Transaction.atomic**: Все операции с БД выполняются в транзакциях

- Запрет операций с несуществующими кошельками

- Валидация типа операции (DEPOSIT/WITHDRAW)

## 📦 Миграции

Миграции применяются автоматически при старте контейнера

## 🔧 Переменные окружения

Настройки в .env файле:

```ini
DEBUG=0
SECRET_KEY=your-secret-key
DB_ENGINE=django.db.backends.postgresql

POSTGRES_HOST=db
POSTGRES_PORT=5432
POSTGRES_DB=wallet_db
POSTGRES_USER=your-user
POSTGRES_PASSWORD=your-password
```

## 📌 Примечания

- Все суммы хранятся в DECIMAL(16,2)

- UUID используется в качестве первичного ключа
