import uvicorn
from fastapi import FastAPI, Depends, HTTPException
from authx import AuthX, AuthXConfig
from fastapi.openapi.models import Response
from pydantic import BaseModel

app = FastAPI()

config = AuthXConfig()
config.JWT_SECRET_KEY = "SECRET_KEY"
config.JWT_ACCESS_COOKIE_NAME = "my_access_token"
config.JWT_TOKEN_LOCATION = ["cookies"]

security = AuthX(config=config)

class Base(BaseModel):
    pass

class UserLoginScheme(Base):
    username: str
    password: str

@app.post("/login")
def login(cred: UserLoginScheme, response: Response):
    if cred.username == "test" and cred.password == "test":
        token = security.create_access_token(uid="1234")
        return {"access_token": token}
    raise HTTPException(status_code=401, detail="Incorrect username or password")

@app.get("/protected")
def protected():
    ...

if __name__ == "__main__":
    uvicorn.run(app)