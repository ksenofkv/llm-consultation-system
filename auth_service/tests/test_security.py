# auth_service/tests/test_security.py

# auth_service/tests/test_security.py

from app.core.security import (
    create_access_token,
    decode_token,
    hash_password,
    verify_password,
)


def test_password_hash_is_created():
    password_hash = hash_password("mysecret")

    assert password_hash is not None


def test_password_hash_not_equal_original_password():
    password = "mysecret"
    password_hash = hash_password(password)

    assert password_hash != password


def test_verify_password_with_correct_password():
    password = "mysecret"
    password_hash = hash_password(password)

    assert verify_password(password, password_hash) is True


def test_verify_password_with_wrong_password():
    password_hash = hash_password("mysecret")

    assert verify_password("wrong_password", password_hash) is False


def test_jwt_token_is_created():
    token = create_access_token(subject=42, role="user")

    assert token is not None
    assert isinstance(token, str)


def test_jwt_contains_sub():
    token = create_access_token(subject=42, role="user")
    payload = decode_token(token)

    assert "sub" in payload
    assert payload["sub"] == "42"


def test_jwt_contains_role():
    token = create_access_token(subject=42, role="user")
    payload = decode_token(token)

    assert "role" in payload
    assert payload["role"] == "user"


def test_jwt_contains_iat():
    token = create_access_token(subject=42, role="user")
    payload = decode_token(token)

    assert "iat" in payload


def test_jwt_contains_exp():
    token = create_access_token(subject=42, role="user")
    payload = decode_token(token)

    assert "exp" in payload


def test_jwt_exp_greater_than_iat():
    token = create_access_token(subject=42, role="user")
    payload = decode_token(token)

    assert payload["exp"] > payload["iat"]
