from fastapi import APIRouter, Body, HTTPException, Response, Depends
from starlette import status

from auth_service.src.core.security import security, verify_password
from auth_service.src.models.crud import register_user, get_users, get_user_by_username
from auth_service.src.schemas.user import UserLoginSchema, UserResponse

router = APIRouter()


@router.post("/login")
async def login(cred: UserLoginSchema, response: Response):
    """
    Аутентификация пользователя.
    
    Args:
        cred: Данные для входа (username, password)
        response: HTTP response для установки cookie
        
    Returns:
        dict: Access token
        
    Raises:
        HTTPException: 404 если пользователь не найден
        HTTPException: 401 если пароль неверный
    """
    user = await get_user_by_username(username=cred.username)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    # Проверяем пароль с помощью хеширования
    if not verify_password(cred.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password"
        )

    # Создаём токен используя username как идентификатор
    token = security.create_access_token(uid=user.username)
    response.set_cookie(
        key=security.config.JWT_ACCESS_COOKIE_NAME,
        value=token,
        httponly=True,
        secure=security.config.JWT_COOKIE_SECURE,
        samesite="lax"
    )
    
    return {"access_token": token, "token_type": "bearer"}


@router.post("/register")
async def register(
    username: str = Body(..., embed=True, min_length=3, max_length=255),
    password: str = Body(..., embed=True, min_length=6, max_length=255)
):
    """
    Регистрация нового пользователя.
    
    Args:
        username: Имя пользователя (3-255 символов)
        password: Пароль (6-255 символов)
        
    Returns:
        dict: Сообщение об успешной регистрации
        
    Raises:
        HTTPException: 400 если пользователь уже существует
    """
    try:
        await register_user(username=username, password=password)
        return {"message": f"User created successfully for {username}"}
    except Exception as e:
        if "already exists" in str(e):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"User with username '{username}' already exists"
            )
        raise


@router.get("/users", response_model=list[UserResponse])
async def get_all_users():
    """
    Получение списка всех пользователей.
    
    Returns:
        list[UserResponse]: Список пользователей
    """
    users = await get_users()
    return users
