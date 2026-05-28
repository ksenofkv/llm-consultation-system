# bot_service/app/services/openrouter_client.py

"""
Клиент OpenRouter API для Bot Service.

Здесь:
- выполняются запросы к OpenRouter
- формируется payload chat/completions
- отправляются HTTP-запросы через httpx
- обрабатываются ошибки сети и API

Файл НЕ:
- содержит aiogram handlers
- содержит Celery tasks
- проверяет JWT
"""

# Асинхронный HTTP клиент
import httpx

# Настройки приложения
from app.core.config import settings


async def call_openrouter(
    prompt: str,
) -> str:
    """
    Отправка запроса в OpenRouter API.

    На вход:
    - prompt пользователя

    Возвращает:
    - текст ответа LLM

    Ошибки:
    - RuntimeError при сетевых ошибках
    - RuntimeError при ошибках OpenRouter API
    """

    # Endpoint OpenRouter
    url = (
        f"{settings.openrouter_base_url}"
        "/chat/completions"
    )

    # Заголовки HTTP запроса
    headers = {
        "Authorization": (
            f"Bearer {settings.openrouter_api_key}"
        ),
        "HTTP-Referer": settings.openrouter_site_url,
        "X-Title": settings.openrouter_app_name,
        "Content-Type": "application/json",
    }

    # Payload OpenRouter
    payload = {
        "model": settings.openrouter_model,
        "messages": [
            {
                "role": "user",
                "content": prompt,
            }
        ],
    }

    try:

        # Асинхронный HTTP клиент
        async with httpx.AsyncClient(
            timeout=60.0
        ) as client:

            # POST запрос в OpenRouter
            response = await client.post(
                url=url,
                headers=headers,
                json=payload,
            )

        # Проверка HTTP статуса
        if response.status_code != 200:

            raise RuntimeError(
                "OpenRouter API error: "
                f"{response.status_code} "
                f"{response.text}"
            )

        # JSON ответ API
        data = response.json()

        # Извлечение текста ответа LLM
        answer = (
            data["choices"][0]["message"]["content"]
        )

        return answer

    # Ошибки сети / timeout
    except httpx.RequestError as exc:

        raise RuntimeError(
            "Network error while calling OpenRouter"
        ) from exc

    # Ошибки структуры ответа
    except (
        KeyError,
        IndexError,
        TypeError,
    ) as exc:

        raise RuntimeError(
            "Invalid OpenRouter response format"
        ) from exc