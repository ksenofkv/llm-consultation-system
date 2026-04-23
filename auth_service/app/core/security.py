# auth_service/app/core/security.py
"""
Функции безопасности: хеширование паролей и работа с JWT.
Используется как строительный блок в usecases и dependencies.
"""

from datetime import datetime, timedelta, timezone
from typing import Any, Union

from jose import jwt, JWTError, ExpiredSignatureError
from passlib.context import CryptContext

from app.core.config import settings

# =============================================================================
# Настройка хеширования паролей (bcrypt через passlib)
# =============================================================================

pwd_context = CryptContext(
    schemes=["bcrypt"],           # Используем bcrypt как единственный алгоритм
    deprecated="auto",            # Автоматически помечать устаревшие хеши
    bcrypt__rounds=12,            # Количество раундов (баланс безопасность/скорость)
)


# =============================================================================
# Функции работы с паролями
# =============================================================================

def hash_password(password: str) -> str:
    """
    Хеширует пароль с использованием bcrypt.
    
    Args:
        password: Исходный пароль в открытом виде.
        
    Returns:
        str: Хеш пароля (формат $2b$12$...).
        
    Example:
        >>> hash = hash_password("my_secret")
        >>> isinstance(hash, str)
        True
    """
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Проверяет соответствие пароля хешу.
    
    Args:
        plain_password: Пароль, введённый пользователем.
        hashed_password: Хеш из базы данных.
        
    Returns:
        bool: True, если пароль верный; False иначе.
        
    Example:
        >>> verify_password("my_secret", hash_password("my_secret"))
        True
        >>> verify_password("wrong_pass", hash_password("my_secret"))
        False
    """
    return pwd_context.verify(plain_password, hashed_password)


# =============================================================================
# Функции работы с JWT-токенами
# =============================================================================

def create_access_token(
    subject: Union[str, int],
    role: str,
    expires_delta: timedelta | None = None
) -> str:
    """
    Создаёт подписанный JWT-токен с обязательными полями.
    
    Обязательные claims (поля токена):
    - sub (subject): идентификатор пользователя (строка)
    - role: роль пользователя (например, "user", "admin")
    - iat (issued at): время выпуска токена (UTC)
    - exp (expiration): время истечения токена (UTC)
    
    Args:
        subject: ID пользователя (будет преобразован в строку).
        role: Роль пользователя.
        expires_delta: Опциональная длительность жизни токена.
                      Если None, используется ACCESS_TOKEN_EXPIRE_MINUTES из config.
    
    Returns:
        str: Подписанный JWT-токен (строка формата header.payload.signature).
        
    Raises:
        ValueError: Если JWT_SECRET не задан.
    """
    if not settings.JWT_SECRET:
        raise ValueError("JWT_SECRET must be configured")
    
    # Вычисляем время истечения
    if expires_delta is None:
        expires_delta = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    expire = datetime.now(timezone.utc) + expires_delta
    
    # Формируем payload с обязательными полями
    to_encode = {
        "sub": str(subject),      # subject: идентификатор пользователя (всегда строка)
        "role": role,             # роль для RBAC-проверок
        "iat": datetime.now(timezone.utc),  # issued at
        "exp": expire,            # expiration time
    }
    
    # Кодируем и подписываем токен
    encoded_jwt = jwt.encode(
        to_encode,
        settings.JWT_SECRET,
        algorithm=settings.JWT_ALG
    )
    
    return encoded_jwt


def decode_token(token: str) -> dict[str, Any]:
    """
    Декодирует и валидирует JWT-токен.
    
    Проверяет:
    - Корректность подписи (алгоритм и секрет)
    - Время жизни токена (exp claim)
    - Наличие обязательных полей
    
    Args:
        token: JWT-токен из заголовка Authorization.
        
    Returns:
        dict: Payload токена с полями sub, role, iat, exp.
        
    Raises:
        jose.jwt.JWTError: Если токен невалиден (неверная подпись, формат).
        jose.jwt.ExpiredSignatureError: Если токен истёк.
        ValueError: Если в токене отсутствуют обязательные поля.
        
    Example:
        >>> payload = decode_token("eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...")
        >>> payload["sub"]
        '42'
        >>> payload["role"]
        'user'
    """
    if not settings.JWT_SECRET:
        raise ValueError("JWT_SECRET must be configured")
    
    try:
        # Декодируем с автоматической проверкой exp и подписи
        payload = jwt.decode(
            token,
            settings.JWT_SECRET,
            algorithms=[settings.JWT_ALG],
            options={"verify_exp": True}  # Явно включаем проверку времени жизни
        )
        
        # Валидируем наличие обязательных полей
        required_claims = {"sub", "role", "iat", "exp"}
        missing_claims = required_claims - payload.keys()
        if missing_claims:
            raise ValueError(f"Token missing required claims: {missing_claims}")
        
        return payload
        
    except ExpiredSignatureError:
        # Перебрасываем как есть — вызывающий код обработает как 401
        raise
    except JWTError as e:
        # Любая другая ошибка декодирования (неверная подпись, формат и т.д.)
        raise JWTError(f"Invalid token: {str(e)}") from e


# =============================================================================
# Вспомогательные функции (опционально, для удобства)
# =============================================================================

def get_token_expire_delta(minutes: int | None = None) -> timedelta:
    """
    Возвращает timedelta для времени жизни токена.
    
    Utility-функция для тестов или кастомной логики выпуска токенов.
    """
    if minutes is None:
        minutes = settings.ACCESS_TOKEN_EXPIRE_MINUTES
    return timedelta(minutes=minutes)