from contextlib import asynccontextmanager

from fastapi import FastAPI
from auth_service.src.database import engine
from auth_service.src.models.user import Base

from auth_service.src.api import main_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)
    yield

app = FastAPI(lifespan=lifespan)
app.include_router(main_router)






