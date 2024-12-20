from typing import Annotated, Optional

from pydantic import BaseModel, EmailStr, StringConstraints
from api.v1.schemas.base_schema import BaseResponseModel


class RegisterRequest(BaseModel):
    email: EmailStr
    password: Optional[str] = None
    username: Annotated[str, StringConstraints(max_length=70)]


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class TokenRefreshRequest(BaseModel):
    refresh_token: str


class TokenRefreshResponse(BaseResponseModel):
    access_token: str


class AuthResponseData(BaseModel):
    id: str
    email: EmailStr
    username: str


class AuthResponse(BaseResponseModel):
    access_token: str
    refresh_token: str
    data: AuthResponseData
