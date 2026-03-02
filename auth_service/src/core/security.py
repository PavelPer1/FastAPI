from passlib.context import CryptContext
from authx import AuthX, AuthXConfig

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    """Хеширует пароль используя bcrypt"""
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Проверяет соответствие пароля хешу"""
    return pwd_context.verify(plain_password, hashed_password)


class SecurityConfig(AuthXConfig):
    """Конфигурация безопасности"""
    JWT_SECRET_KEY: str = "your-secret-key-change-in-production"
    JWT_ACCESS_COOKIE_NAME: str = "access_token"
    JWT_TOKEN_LOCATION: list = ["cookies", "headers"]
    JWT_ACCESS_COOKIE_PATH: str = "/"
    JWT_COOKIE_SECURE: bool = False  # Установить True в production с HTTPS


config = SecurityConfig()
security = AuthX(config=config)
