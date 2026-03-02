from contextlib import asynccontextmanager

from fastapi import FastAPI
from auth_service.src.database import engine
from auth_service.src.models.user import Base
from auth_service.src.api.auth import router as auth_router
from auth_service.src.api.register import router as register_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifecycle manager для приложения.
    Создаёт таблицы в БД при запуске.
    """
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)
    yield


app = FastAPI(
    title="Auth Service",
    description="Микросервис для авторизации и регистрации пользователей",
    version="1.0.0",
    lifespan=lifespan
)

# Подключаем роутеры
app.include_router(auth_router, prefix="/api/auth", tags=["Authentication"])
app.include_router(register_router, prefix="/api/register", tags=["Registration"])


@app.get("/health")
async def health_check():
    """Проверка работоспособности сервиса"""
    return {"status": "healthy", "service": "auth_service"}
