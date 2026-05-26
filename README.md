# llm-consultation-system


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