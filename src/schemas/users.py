from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional


class Base(BaseModel):
    pass

class UserLoginScheme(Base):
    username: str
    password: str

class UserBase(BaseModel):
    username: str
    email: EmailStr
    full_name: Optional[str] = None
    phone: Optional[str] = None
    department: Optional[str] = None


class UserCreate(UserBase):
    pass


class UserResponse(UserBase):
    id: int
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True


class ExcelUploadResponse(BaseModel):
    total_records: int
    successful_records: int
    failed_records: int
    errors: list[str]
