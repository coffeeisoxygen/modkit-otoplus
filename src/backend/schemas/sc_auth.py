"""schemas for authentication, when user logs in."""

from pydantic import BaseModel


class AuthLogin(BaseModel):
    username: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
