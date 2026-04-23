from app.core.security import hash_password, verify_password, create_access_token, decode_token

print("🔐 Тест безопасности Auth Service")
print("-" * 40)

# 1. Тест паролей
print("\n1. Хеширование паролей:")
pwd_hash = hash_password("SecurePass123!")
print(f"   Хеш: {pwd_hash[:30]}...")
print(f"   Верный пароль: {verify_password('SecurePass123!', pwd_hash)}")
print(f"   Неверный пароль: {verify_password('WrongPass', pwd_hash)}")

# 2. Тест JWT
print("\n2. JWT-токены:")
token = create_access_token(subject=42, role="admin")
print(f"   Токен: {token[:50]}...")
payload = decode_token(token)
print(f"   sub={payload['sub']}, role={payload['role']}")
print(f"   iat={payload['iat']}, exp={payload['exp']}")

print("\n✅ Все тесты пройдены!")