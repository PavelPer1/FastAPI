from auth_service.src.database import new_session
from src.models.database.users import User
from sqlalchemy import select


async def register_user(
        username: str,
        password: str
):
    async with new_session() as session:
        new_user = User(
            username=username,
            password=password,
        )
        session.add(new_user)
        await session.commit()
        return {"message": "User created successfully"}

async def get_users():
    async with new_session() as session:
        result = await session.execute(select(User))
        users = result.scalars().all()
        return users


async def get_user(username: str):
    async with new_session() as session:
        return await session.get(User, username)
