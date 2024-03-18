from datetime import datetime

from pydantic import BaseModel, EmailStr, UUID4, Field, field_validator


class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str


class UserBase(BaseModel):
    id: int
    email: EmailStr
    username: str


class TokenBase(BaseModel):
    token: UUID4 = Field(alias='access_token')
    expires: datetime
    token_type: str | None = 'bearer'

    class Config:
        allow_population_by_field_name = True

    @field_validator('token')
    def hexlify(cls, value):
        return value.hex


class User(UserBase):
    token: TokenBase = {}
