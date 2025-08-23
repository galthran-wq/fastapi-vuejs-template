from pydantic import BaseModel, EmailStr
from uuid import UUID
from datetime import datetime
from typing import Optional, Union


class UserResponse(BaseModel):
    id: UUID
    email: Optional[str] = None
    is_verified: bool
    is_superuser: bool
    created_at: datetime

    class Config:
        from_attributes = True


class UserRegisterRequest(BaseModel):
    email: EmailStr
    password: str


class UserLoginRequest(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserResponse


class CreateUserRequest(BaseModel):
    email: EmailStr
    password: str


class CreateUserResponse(BaseModel):
    success: bool
    message: str
    user: Optional[UserResponse] = None


class DeleteUserRequest(BaseModel):
    user_identifier: Union[UUID, EmailStr]


class DeleteUserResponse(BaseModel):
    success: bool
    message: str 