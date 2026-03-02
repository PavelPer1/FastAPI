from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional


class UserLoginSchema(BaseModel):
    """Схема для входа пользователя"""
    username: str
    password: str


class UserBase(BaseModel):
    """Базовая схема пользователя"""
    username: str
    email: Optional[EmailStr] = None
    full_name: Optional[str] = None
    phone: Optional[str] = None
    department: Optional[str] = None


class UserCreate(UserBase):
    """Схема для создания пользователя"""
    password: str


class UserResponse(UserBase):
    """Схема ответа с данными пользователя"""
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True


class UserRegisterResponse(BaseModel):
    """Схема ответа после регистрации"""
    message: str
    username: str


class ExcelUploadResponse(BaseModel):
    """Схема ответа после загрузки Excel"""
    success: bool
    message: str
    registered_users: list[dict]
    skipped_users: list[dict]
    failed_users: list[dict]
    statistics: dict
