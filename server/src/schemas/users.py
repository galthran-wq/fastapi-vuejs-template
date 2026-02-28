from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, EmailStr


class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    email: str | None = None
    is_verified: bool
    is_superuser: bool
    created_at: datetime


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
    user: UserResponse | None = None


class DeleteUserRequest(BaseModel):
    user_identifier: UUID | EmailStr


class DeleteUserResponse(BaseModel):
    success: bool
    message: str
