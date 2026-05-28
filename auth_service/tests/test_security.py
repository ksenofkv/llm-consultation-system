# auth_service/tests/test_security.py

"""
Модульные тесты безопасности Auth Service.

Проверяется:
- хеширование пароля
- проверка правильного пароля
- отказ при неправильном пароле
- создание JWT
- декодирование JWT
- наличие обязательных полей sub, role, iat, exp
"""

from app.core.security import (
    create_access_token,
    decode_token,
    hash_password,
    verify_password,
)


def test_password_hashing():
    """
    Проверяет, что пароль:
    - хешируется
    - хеш не равен исходному паролю
    - правильный пароль проходит проверку
    - неправильный пароль не проходит проверку
    """

    password = "mysecret"

    password_hash = hash_password(password)

    assert password_hash != password
    assert verify_password(password, password_hash) is True
    assert verify_password("wrong_password", password_hash) is False


def test_jwt_creation_and_decoding():
    """
    Проверяет создание и декодирование JWT.

    JWT должен содержать:
    - sub
    - role
    - iat
    - exp
    """

    token = create_access_token(
        subject=42,
        role="user",
    )

    payload = decode_token(token)

    assert payload["sub"] == "42"
    assert payload["role"] == "user"

    assert "iat" in payload
    assert "exp" in payload

    assert payload["exp"] > payload["iat"]