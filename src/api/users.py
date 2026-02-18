from authx import AuthX, AuthXConfig
from fastapi import APIRouter
from fastapi import HTTPException, Response

from src.schemas.users import UserLoginScheme

router = APIRouter()

config = AuthXConfig()
config.JWT_SECRET_KEY = "SECRET_KEY"
config.JWT_ACCESS_COOKIE_NAME = "my_access_token"
config.JWT_TOKEN_LOCATION = ["cookies"]

security = AuthX(config=config)

@router.post("/login")
def login(cred: UserLoginScheme, response: Response):
    if cred.username == "test" and cred.password == "test":
        token = security.create_access_token(uid="1234")
        response.set_cookie(config.JWT_ACCESS_COOKIE_NAME, token)
        return {"access_token": token}
    raise HTTPException(status_code=401, detail="Incorrect username or password")