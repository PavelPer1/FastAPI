from auth_service.src.database import new_session
from auth_service.src.models.user import User
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


# Добавьте в auth_service.src.models.crud

async def get_user_by_username(username: str):
    """
    Проверяет, существует ли пользователь с таким username
    """
    async with new_session() as session:
        from auth_service.src.models.user import User  # Импортируйте вашу модель
        from sqlalchemy import select

        result = await session.execute(
            select(User).where(User.username == username)
        )
        user = result.scalar_one_or_none()
        return user

async def get_users():
    async with new_session() as session:
        result = await session.execute(select(User))
        users = result.scalars().all()
        return users


async def get_user(username: str):
    async with new_session() as session:
        return await session.get(User, username)
