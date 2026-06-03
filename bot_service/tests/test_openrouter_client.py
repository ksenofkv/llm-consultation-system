import httpx
import pytest
import respx
from app.services.openrouter_client import call_openrouter


@pytest.fixture
def openrouter_route():
    route = respx.post("https://openrouter.ai/api/v1/chat/completions").mock(
        return_value=httpx.Response(
            200,
            json={"choices": [{"message": {"content": "Тестовый ответ модели"}}]},
        )
    )

    return route


@pytest.mark.asyncio
@respx.mock
async def test_openrouter_http_request_was_sent(
    openrouter_route,
):
    await call_openrouter("Привет")

    assert openrouter_route.called is True


@pytest.mark.asyncio
@respx.mock
async def test_openrouter_returns_string(
    openrouter_route,
):
    result = await call_openrouter("Привет")

    assert isinstance(result, str)


@pytest.mark.asyncio
@respx.mock
async def test_openrouter_extracts_message_content(
    openrouter_route,
):
    result = await call_openrouter("Привет")

    assert result == "Тестовый ответ модели"
