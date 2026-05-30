# LLM Consultation System

Микросервисная система для взаимодействия с Large Language Models (LLM) через Telegram-бота с JWT-аутентификацией, очередями сообщений и асинхронной обработкой запросов.

---

# Описание проекта

Система реализована в виде двух независимых микросервисов:

## Auth Service

Сервис авторизации, реализованный на FastAPI.

Функциональность:

* регистрация пользователей;
* аутентификация пользователей;
* выдача JWT-токенов;
* получение информации о текущем пользователе;
* защита API через JWT.

Auth Service полностью независим от Telegram и может использоваться любыми внешними клиентами.

---

## Bot Service

Telegram-бот, реализованный на Aiogram.

Функциональность:

* прием сообщений от пользователей Telegram;
* сохранение JWT-токена пользователя;
* проверка валидности JWT;
* отправка запросов в очередь RabbitMQ;
* обработка запросов через Celery Worker;
* взаимодействие с LLM через OpenRouter API;
* хранение временных данных в Redis.

Bot Service не хранит пользователей и не обращается напрямую к базе данных Auth Service.

---

# Архитектура системы

```text
Telegram User
      │
      ▼
Telegram Bot (Aiogram)
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
```

## Преимущества архитектуры

* асинхронная обработка запросов;
* отсутствие блокировки Telegram-бота;
* масштабируемость;
* отказоустойчивость;
* разделение ответственности между сервисами.

---

# Используемые технологии

## Backend

* Python 3.12
* FastAPI
* SQLAlchemy Async
* SQLite
* Pydantic
* Pydantic Settings

## Безопасность

* JWT
* python-jose
* Passlib
* bcrypt

## Telegram

* Aiogram 3

## Очереди и фоновые задачи

* RabbitMQ
* Celery
* Redis

## Контейнеризация

* Docker
* Docker Compose

## Тестирование

* Pytest
* Pytest Asyncio
* HTTPX
* RESPX
* Fakeredis
* Pytest Mock

---

# Структура проекта

```text
llm_consultation_system/
│
├── auth_service/
│   ├── app/
│   ├── tests/
│   ├── pyproject.toml
│   ├── pytest.ini
│   └── .env
│
├── bot_service/
│   ├── app/
│   ├── tests/
│   ├── pyproject.toml
│   ├── pytest.ini
│   └── .env
│
├── docker-compose.yml
├── README.md
└── screenshots/
```

---

# Auth Service

## Регистрация пользователя

### Запрос

```http
POST /auth/register
```

```json
{
  "email": "user@example.com",
  "password": "password123"
}
```

---

## Авторизация

### Запрос

```http
POST /auth/login
```

Используется:

```text
OAuth2PasswordRequestForm
```

Пример данных:

```text
username=user@example.com
password=password123
```

Ответ:

```json
{
  "access_token": "<jwt>",
  "token_type": "bearer"
}
```

---

## Получение текущего пользователя

### Запрос

```http
GET /auth/me
```

Заголовок:

```text
Authorization: Bearer <jwt>
```

---

# JWT

Пример полезной нагрузки токена:

```json
{
  "sub": "1",
  "role": "user",
  "iat": 1710000000,
  "exp": 1710003600
}
```

При проверке токена контролируются:

* корректность подписи;
* срок действия;
* наличие поля `sub`;
* наличие поля `role`.

---

# Bot Service

## Пользовательский сценарий

1. Пользователь регистрируется через Swagger Auth Service.
2. Пользователь получает JWT-токен.
3. В Telegram выполняет команду:

```text
/token <jwt>
```

4. JWT сохраняется в Redis.
5. Пользователь отправляет запрос боту.
6. Бот проверяет токен.
7. Запрос отправляется в RabbitMQ.
8. Celery Worker обрабатывает задачу.
9. OpenRouter возвращает ответ LLM.
10. Ответ отправляется пользователю в Telegram.

---

# Redis

Redis используется для:

* хранения JWT пользователей;
* хранения промежуточных данных;
* backend-хранилища результатов Celery.

---

# RabbitMQ и Celery

Используются для организации очередей задач и асинхронного взаимодействия между компонентами системы.

Преимущества:

* неблокирующая обработка сообщений;
* масштабируемость;
* распределение нагрузки;
* возможность обработки большого количества запросов.

---

# Запуск проекта

## Сборка контейнеров

```bash
docker compose build
```

## Запуск

```bash
docker compose up
```

## Запуск в фоне

```bash
docker compose up -d
```

## Остановка

```bash
docker compose down
```

---

# Swagger UI

После запуска Auth Service:

```text
http://localhost:8000/docs
```

---

# RabbitMQ Management

После запуска:

```text
http://localhost:15672
```

Логин:

```text
guest
```

Пароль:

```text
guest
```

---

# Тестирование Auth Service

## Запуск тестов

Из директории `auth_service`:

```bash
pytest -v
```

## Реализованные тесты

### Модульные тесты

Проверяют:

* создание хеша пароля;
* отличие хеша от исходного пароля;
* успешную проверку корректного пароля;
* отклонение неверного пароля;
* создание JWT;
* наличие полей `sub`, `role`, `iat`, `exp`.

### Интеграционные тесты

Проверяют:

* регистрацию пользователя;
* авторизацию пользователя;
* получение JWT;
* доступ к `/auth/me`.

### Негативные тесты

Проверяют:

* повторную регистрацию (409);
* неверный пароль (401);
* отсутствие токена (401);
* невалидный токен (401).

### Результат

```text
========================
7 passed
========================
```

Все тесты успешно пройдены.

---

# Тестирование Bot Service

## Запуск тестов

Из директории `bot_service`:

```bash
pytest -v
```

## Реализованные тесты

Проверяются следующие компоненты:

### JWT Validation

* корректный JWT;
* истекший JWT;
* невалидный JWT.

### Telegram Handlers

* обработка команды `/start`;
* сохранение JWT через `/token`;
* обработка пользовательских сообщений.

### Redis Integration

* сохранение токенов;
* получение токенов;
* работа через `fakeredis`.

### Celery Integration

* постановка задач в очередь;
* корректный вызов Celery-задач.

### OpenRouter Integration

* успешная обработка HTTP-запросов;
* обработка ошибок внешнего API;
* мокирование через RESPX.

### Результат

```text
========================
20 passed
========================
```

Все тесты успешно пройдены.

---

# Дополнительно установленные зависимости для тестирования

## Auth Service

```bash
pip install pytest
pip install pytest-asyncio
pip install httpx
pip install python-multipart
pip install pydantic[email]
pip install python-jose[cryptography]
pip install bcrypt==4.0.1
```

## Bot Service

```bash
pip install pytest pytest-asyncio pytest-mock
pip install fakeredis celery
pip install respx httpx
pip install "python-jose[cryptography]"
```

---

# Скриншоты

Рекомендуется приложить:

* Swagger Register
* Swagger Login
* Swagger Me
* Telegram Bot
* RabbitMQ Dashboard
* Результаты тестирования Auth Service
* Результаты тестирования Bot Service

---

# Итоги проекта

В рамках проекта была разработана полноценная микросервисная система для взаимодействия с LLM через Telegram.

Реализованы:

* JWT-аутентификация пользователей;
* регистрация и авторизация через FastAPI;
* Telegram-бот на Aiogram;
* асинхронная обработка запросов;
* RabbitMQ + Celery;
* Redis для хранения токенов и промежуточных данных;
* интеграция с OpenRouter API;
* модульное, интеграционное и негативное тестирование;
* контейнеризация через Docker Compose.

Все реализованные тесты успешно проходят:

```text
Auth Service: 7 passed
Bot Service: 20 passed
Итого: 27 passed
```


