import os
from contextlib import asynccontextmanager

from fastapi import FastAPI
from sqlalchemy import create_engine, text
from src.models.database.database import engine
from src.models.database.users import Base

from src.api import main_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)
    yield

app = FastAPI(lifespan=lifespan)
app.include_router(main_router)






