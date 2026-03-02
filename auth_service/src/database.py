from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from auth_service.src.core.config import config

engine = create_async_engine(
    url=f'postgresql+asyncpg://{config.DB_USER}:{config.DB_PASSWORD}@{config.DB_HOST}:{config.DB_PORT}/{config.DB_NAME}',
    echo=config.DEBUG
)

new_session = async_sessionmaker(bind=engine, expire_on_commit=False)
