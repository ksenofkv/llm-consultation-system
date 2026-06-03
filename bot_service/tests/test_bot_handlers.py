import fakeredis.aioredis
import pytest


class FakeUser:
    def __init__(self, user_id=777):
        self.id = user_id


class FakeChat:
    def __init__(self, chat_id=555):
        self.id = chat_id


class FakeMessage:
    def __init__(
        self,
        text,
        user_id=777,
        chat_id=555,
    ):
        self.text = text
        self.from_user = FakeUser(user_id)
        self.chat = FakeChat(chat_id)
        self.answers = []

    async def answer(self, text):
        self.answers.append(text)


@pytest.fixture
async def token_command_context(mocker):
    from app.bot import handlers

    fake_redis = fakeredis.aioredis.FakeRedis(decode_responses=True)

    mocker.patch(
        "app.bot.handlers.get_redis",
        return_value=fake_redis,
    )

    mocker.patch(
        "app.bot.handlers.decode_and_validate",
        return_value={"sub": "123"},
    )

    message = FakeMessage(
        "/token test.jwt.token",
        user_id=777,
        chat_id=555,
    )

    await handlers.token_handler(message)

    return {
        "redis": fake_redis,
        "message": message,
    }


@pytest.fixture
async def text_without_token_context(mocker):
    from app.bot import handlers

    fake_redis = fakeredis.aioredis.FakeRedis(decode_responses=True)

    mocker.patch(
        "app.bot.handlers.get_redis",
        return_value=fake_redis,
    )

    delay_mock = mocker.patch("app.bot.handlers.llm_request.delay")

    message = FakeMessage(
        "Привет",
        user_id=777,
        chat_id=555,
    )

    await handlers.text_handler(message)

    return {
        "redis": fake_redis,
        "message": message,
        "delay_mock": delay_mock,
    }


@pytest.fixture
async def text_with_token_context(mocker):
    from app.bot import handlers

    fake_redis = fakeredis.aioredis.FakeRedis(decode_responses=True)

    await fake_redis.set(
        "token:777",
        "saved.jwt.token",
    )

    mocker.patch(
        "app.bot.handlers.get_redis",
        return_value=fake_redis,
    )

    mocker.patch(
        "app.bot.handlers.decode_and_validate",
        return_value={"sub": "123"},
    )

    delay_mock = mocker.patch("app.bot.handlers.llm_request.delay")

    message = FakeMessage(
        "Расскажи про FastAPI",
        user_id=777,
        chat_id=555,
    )

    await handlers.text_handler(message)

    return {
        "redis": fake_redis,
        "message": message,
        "delay_mock": delay_mock,
    }


@pytest.mark.asyncio
async def test_token_command_saves_token_to_redis(
    token_command_context,
):
    saved_token = await token_command_context["redis"].get("token:777")

    assert saved_token == "test.jwt.token"


@pytest.mark.asyncio
async def test_token_command_uses_correct_redis_key(
    token_command_context,
):
    saved_token = await token_command_context["redis"].get("token:777")

    assert saved_token is not None


@pytest.mark.asyncio
async def test_token_command_sends_one_answer(
    token_command_context,
):
    message = token_command_context["message"]

    assert len(message.answers) == 1


@pytest.mark.asyncio
async def test_token_command_sends_success_message(
    token_command_context,
):
    message = token_command_context["message"]

    assert "токен принят" in message.answers[0].lower()


@pytest.mark.asyncio
async def test_text_without_token_does_not_call_celery(
    text_without_token_context,
):
    delay_mock = text_without_token_context["delay_mock"]

    assert delay_mock.call_count == 0


@pytest.mark.asyncio
async def test_text_without_token_sends_one_answer(
    text_without_token_context,
):
    message = text_without_token_context["message"]

    assert len(message.answers) == 1


@pytest.mark.asyncio
async def test_text_without_token_sends_access_denied_message(
    text_without_token_context,
):
    message = text_without_token_context["message"]

    assert "доступ запрещён" in message.answers[0].lower()


@pytest.mark.asyncio
async def test_text_without_token_mentions_token_command(
    text_without_token_context,
):
    message = text_without_token_context["message"]

    assert "/token <jwt>" in message.answers[0]


@pytest.mark.asyncio
async def test_text_with_token_calls_celery_once(
    text_with_token_context,
):
    delay_mock = text_with_token_context["delay_mock"]

    assert delay_mock.call_count == 1


@pytest.mark.asyncio
async def test_text_with_token_passes_correct_chat_id(
    text_with_token_context,
):
    delay_mock = text_with_token_context["delay_mock"]

    _, kwargs = delay_mock.call_args

    assert kwargs["tg_chat_id"] == 555


@pytest.mark.asyncio
async def test_text_with_token_passes_correct_prompt(
    text_with_token_context,
):
    delay_mock = text_with_token_context["delay_mock"]

    _, kwargs = delay_mock.call_args

    assert kwargs["prompt"] == "Расскажи про FastAPI"


@pytest.mark.asyncio
async def test_text_with_token_sends_one_answer(
    text_with_token_context,
):
    message = text_with_token_context["message"]

    assert len(message.answers) == 1


@pytest.mark.asyncio
async def test_text_with_token_sends_request_accepted_message(
    text_with_token_context,
):
    message = text_with_token_context["message"]

    assert "запрос принят" in message.answers[0].lower()
