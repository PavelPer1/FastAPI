from authx import AuthX, AuthXConfig
from fastapi import APIRouter, Body
from fastapi import HTTPException, Response
from starlette import status

from src.models.database.crud import register_user, get_users, get_user
from src.schemas.users import UserLoginScheme

router = APIRouter()

config = AuthXConfig()
config.JWT_SECRET_KEY = "SECRET_KEY"
config.JWT_ACCESS_COOKIE_NAME = "my_access_token"
config.JWT_TOKEN_LOCATION = ["cookies"]

security = AuthX(config=config)


@router.post("/login")
async def login(cred: UserLoginScheme, response: Response):
    user = await get_user(username=cred.username)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    if cred.password == user.password:  # В реальном проекте используйте хеширование!
        # Используем username как идентификатор (так как это primary_key)
        token = security.create_access_token(uid=user.username)  # ИСПРАВЛЕНО: user.username вместо user.id
        response.set_cookie(config.JWT_ACCESS_COOKIE_NAME, token)
        return {"access_token": token}

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Incorrect username or password"
    )


@router.post("/register")
async def register(
        username: str = Body(embed=True),
        password: str = Body(embed=True)
):
    await register_user(username=username, password=password)
    return {"message": f"User created successfully for {username}"}

@router.get("/users")
async def get_all_users():
    users = await get_users()
    return users
