import pytest
from jose import jwt

from app.core.config import settings
from app.core.jwt import decode_and_validate


@pytest.fixture
def valid_payload():
    token = jwt.encode(
        {"sub": "123"},
        settings.jwt_secret,
        algorithm=settings.jwt_alg,
    )
    return decode_and_validate(token)


def test_decode_returns_payload(valid_payload):
    assert valid_payload is not None


def test_decode_contains_sub(valid_payload):
    assert "sub" in valid_payload


def test_decode_sub_equals_expected(valid_payload):
    assert valid_payload["sub"] == "123"


def test_decode_invalid_token_raises_error():
    with pytest.raises(ValueError):
        decode_and_validate("not.a.jwt")
