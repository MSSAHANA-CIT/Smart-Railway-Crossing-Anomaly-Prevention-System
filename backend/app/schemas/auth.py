"""Authentication request and response schemas."""

from pydantic import BaseModel, EmailStr, Field

from app.schemas.user import CurrentUserResponse


class LoginRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=1)


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int
    user: CurrentUserResponse
