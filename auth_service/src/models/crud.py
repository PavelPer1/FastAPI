from auth_service.src.database import new_session
from auth_service.src.models.user import User
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from auth_service.src.core.security import hash_password


async def register_user(
    username: str,
    password: str,
    email: str | None = None,
    full_name: str | None = None,
    phone: str | None = None,
    department: str | None = None
) -> User:
    """
    Регистрирует нового пользователя с хешированием пароля.
    
    Returns:
        User: Созданный пользователь
        
    Raises:
        IntegrityError: Если пользователь с таким username уже существует
    """
    async with new_session() as session:
        # Проверяем существование пользователя
        existing_user = await get_user_by_username(username)
        if existing_user:
            raise IntegrityError(
                f"User with username '{username}' already exists",
                params={},
                orig=None
            )
        
        # Хешируем пароль
        hashed_password = hash_password(password)
        
        new_user = User(
            username=username,
            password=hashed_password,
            email=email,
            full_name=full_name,
            phone=phone,
            department=department
        )
        session.add(new_user)
        await session.commit()
        await session.refresh(new_user)
        return new_user


async def get_user_by_username(username: str) -> User | None:
    """
    Получает пользователя по username.
    
    Args:
        username: Имя пользователя
        
    Returns:
        User | None: Пользователь или None если не найден
    """
    async with new_session() as session:
        result = await session.execute(
            select(User).where(User.username == username)
        )
        return result.scalar_one_or_none()


async def get_users() -> list[User]:
    """
    Получает список всех пользователей.
    
    Returns:
        list[User]: Список пользователей
    """
    async with new_session() as session:
        result = await session.execute(select(User))
        return list(result.scalars().all())


async def get_user(username: str) -> User | None:
    """
    Получает пользователя по username (алиас для get_user_by_username).
    
    Args:
        username: Имя пользователя
        
    Returns:
        User | None: Пользователь или None если не найден
    """
    return await get_user_by_username(username)


async def update_user(username: str, **kwargs) -> User | None:
    """
    Обновляет данные пользователя.
    
    Args:
        username: Имя пользователя
        **kwargs: Поля для обновления
        
    Returns:
        User | None: Обновлённый пользователь или None если не найден
    """
    async with new_session() as session:
        user = await get_user_by_username(username)
        if not user:
            return None
        
        for key, value in kwargs.items():
            if hasattr(user, key):
                setattr(user, key, value)
        
        await session.commit()
        await session.refresh(user)
        return user


async def delete_user(username: str) -> bool:
    """
    Удаляет пользователя.
    
    Args:
        username: Имя пользователя
        
    Returns:
        bool: True если удалён, False если не найден
    """
    async with new_session() as session:
        user = await get_user_by_username(username)
        if not user:
            return False
        
        await session.delete(user)
        await session.commit()
        return True
