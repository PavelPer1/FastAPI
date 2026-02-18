from pydantic import BaseModel


class Base(BaseModel):
    pass

class UserLoginScheme(Base):
    username: str
    password: str
