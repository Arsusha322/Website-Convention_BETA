from pydantic import BaseModel, EmailStr, Field, field_validator
from datetime import datetime
import re


class UserBase(BaseModel):
    email: EmailStr = Field(..., example="Arseniy@gmail.com")


class UserCreate(UserBase):
    password: str = Field(..., example="password322")

    @field_validator("password")
    def validate_password(cls, p: str) -> str:
        if not re.match(r"^[A-Za-z0-9]+$", p):
            raise ValueError("Пароль должен содержать только английские буквы и цифры")


        if len(p) < 8:
            raise ValueError("Пароль должен быть минимум 8 символов")


        if not re.search(r"[A-Za-z]", p):
            raise ValueError("Пароль должен содержать хотя бы одну букву")


        if not re.search(r"[0-9]", p):
            raise ValueError("Пароль должен содержать хотя бы одну цифру")

        return p


class UserResponse(UserBase):
    id: int

    class Config:
        from_attributes = True


class UserLogin(UserBase):
    password: str = Field(..., example='password322')

class UserLoginResponse(BaseModel):
    access_token: str
    token_type: str


class UserHistoryCreate(BaseModel):
    file_name: str
    text_result: str

class UserHistoryResponse(BaseModel):
    id: int
    file_name: str
    text_result: str
    created_at: datetime

    class Config:
        from_attributes = True