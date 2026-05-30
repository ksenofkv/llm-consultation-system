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

import httpx

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

    url = f"{settings.openrouter_base_url}/chat/completions"

    headers = {
        "Authorization": (f"Bearer {settings.openrouter_api_key}"),
        "HTTP-Referer": settings.openrouter_site_url,
        "X-Title": settings.openrouter_app_name,
        "Content-Type": "application/json",
    }

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
        async with httpx.AsyncClient(
            timeout=60.0,
            trust_env=False,
        ) as client:
            response = await client.post(
                url=url,
                headers=headers,
                json=payload,
            )

        if response.status_code != 200:
            raise RuntimeError(
                f"OpenRouter API error: {response.status_code} {response.text}"
            )

        data = response.json()

        answer = data["choices"][0]["message"]["content"]

        return answer

    except httpx.RequestError as exc:
        raise RuntimeError("Network error while calling OpenRouter") from exc

    except (
        KeyError,
        IndexError,
        TypeError,
    ) as exc:
        raise RuntimeError("Invalid OpenRouter response format") from exc
