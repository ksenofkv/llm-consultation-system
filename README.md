# llm-consultation-system
Микросервисная система для работы с LLM через Telegram-бота с JWT-аутентификацией.

# Архитектура проекта

Проект состоит из двух независимых сервисов:

Auth Service (FastAPI), отвечает за:
1. Регистрацию пользователей;
2. Аутентификацию пользователей;
3. Выдачу JWT-токенов;
4. Получение информации о текущем пользователе.

Auth Service не зависит от Telegram и может использоваться любыми внешними клиентами.

Bot Service (Aiogram), отвечает за:
1. Приём сообщений из Telegram;
2. Проверку JWT-токена;
3. Отправку запросов к LLM;
4. Взаимодействие с RabbitMQ, Celery и Redis.

Bot Service не хранит пользователей и не обращается напрямую к базе данных Auth Service.

## Технологии
- Backend
- Python 3.12
- FastAPI
- SQLAlchemy Async
- SQLite
- Pydantic
- Pydantic Settings

## Безопасность
- JWT
- python-jose
- Passlib
- bcrypt

## Telegram Bot
- Aiogram 3
- Очереди и фоновые задачи
RabbitMQ
Celery
Redis

## Тестирование
- Pytest
- Pytest Asyncio
- HTTPX

## Контейнеризация
- Docker
- Docker Compose


## Структура проекта

```text
llm_consultation_system/
├── auth_service/
│   ├── app/
│   │   ├── main.py
│   │   ├── core/
│   │   │   ├── config.py
│   │   │   ├── security.py
│   │   │   └── exceptions.py
│   │   ├── db/
│   │   │   ├── base.py
│   │   │   ├── session.py
│   │   │   └── models.py
│   │   ├── schemas/
│   │   │   ├── auth.py
│   │   │   └── user.py
│   │   ├── repositories/
│   │   │   └── users.py
│   │   ├── usecases/
│   │   │   └── auth.py
│   │   └── api/
│   │       ├── deps.py
│   │       ├── routes_auth.py
│   │       └── router.py
│   ├── tests/
│   │   └── ...
│   ├── pyproject.toml
│   ├── pytest.ini
│   └── .env
│
├── bot_service/
│   ├── app/
│   │   ├── main.py
│   │   ├── core/
│   │   │   ├── config.py
│   │   │   └── jwt.py
│   │   ├── infra/
│   │   │   ├── redis.py
│   │   │   └── celery_app.py
│   │   ├── tasks/
│   │   │   └── llm_tasks.py
│   │   ├── services/
│   │   │   └── openrouter_client.py
│   │   └── bot/
│   │       ├── dispatcher.py
│   │       └── handlers.py
│   ├── tests/
│   │   ├── conftest.py
│   │   └── ...
│   ├── pyproject.toml
│   ├── pytest.ini
│   └── .env
│
├── docker-compose.yml
├── README.md
└── screenshots/
    ├── swagger_register.png
    ├── swagger_login.png
    ├── swagger_me.png
    ├── telegram_bot.png
    ├── rabbitmq.png
    └── tests.png

```




Auth Service
Основные маршруты
Регистрация
POST /auth/register

Пример:

{
  "email": "user@example.com",
  "password": "password123"
}
Логин
POST /auth/login

Используется OAuth2PasswordRequestForm.

Пример:

username=user@example.com
password=password123

Ответ:

{
  "access_token": "<jwt>",
  "token_type": "bearer"
}
Информация о пользователе
GET /auth/me

Заголовок:

Authorization: Bearer <jwt>
JWT

Токен содержит:

{
  "sub": "1",
  "role": "user",
  "iat": 1710000000,
  "exp": 1710003600
}

Проверяется:

подпись;
срок действия;
наличие sub;
наличие role.
Bot Service
Пользовательский сценарий
Пользователь регистрируется через Swagger Auth Service.
Пользователь получает JWT.
Пользователь отправляет боту:
/token <jwt>
Токен сохраняется в Redis.
Пользователь отправляет запрос.
Бот валидирует JWT.
Бот публикует задачу в RabbitMQ.
Celery Worker вызывает LLM.
Ответ отправляется пользователю.
RabbitMQ и Celery

Архитектура обработки сообщений:

Telegram User
      │
      ▼
Telegram Bot
      │
      ▼
RabbitMQ
      │
      ▼
Celery Worker
      │
      ▼
OpenRouter API
      │
      ▼
Telegram User

Преимущества:

неблокирующая обработка запросов;
масштабируемость;
устойчивость к нагрузке.
Redis

Redis используется для:

хранения JWT пользователя;
хранения промежуточных данных;
backend Celery результатов.
Запуск проекта
Через Docker Compose

Сборка контейнеров:

docker compose build

Запуск:

docker compose up

Запуск в фоне:

docker compose up -d

Остановка:

docker compose down
Swagger

После запуска Auth Service:

http://localhost:8000/docs
RabbitMQ Management

После запуска:

http://localhost:15672

Логин:

guest

Пароль:

guest
Тестирование
Запуск тестов

Из папки auth_service:

pytest -v
Реализованные тесты
Модульные тесты

Проверяются:

создание хеша пароля;
отличие хеша от исходного пароля;
успешная проверка правильного пароля;
отклонение неправильного пароля;
создание JWT;
наличие sub;
наличие role;
наличие iat;
наличие exp.
Интеграционные тесты

Проверяются:

регистрация пользователя;
логин пользователя;
получение JWT;
доступ к /auth/me по JWT.
Негативные тесты

Проверяются:

повторная регистрация (409);
неверный пароль (401);
отсутствие токена (401);
неверный токен (401).
Результат тестирования
=========================================
7 passed
=========================================

Все тесты успешно пройдены.

Автор

Проект выполнен в рамках учебного задания по разработке микросервисной платформы для взаимодействия с LLM через Telegram-бота с использованием FastAPI, RabbitMQ, Celery и Redis.