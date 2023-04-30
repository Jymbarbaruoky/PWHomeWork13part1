from datetime import datetime
from pydantic import BaseModel, Field, EmailStr


class ContactModel(BaseModel):
    firstname: str = Field(max_length=25)
    lastname: str = Field(max_length=25)
    email: EmailStr
    phone: str
    birthday: datetime
    description: str = Field(max_length=150)


class ContactResponse(BaseModel):
    id: int
    firstname: str
    lastname: str
    email: EmailStr
    phone: str
    birthday: datetime
    description: str
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class UserModel(BaseModel):
    username: str = Field(min_length=3, max_length=16)
    email: str
    password: str = Field(min_length=6, max_length=10)


class UserDb(BaseModel):
    id: int
    username: str
    email: str
    created_at: datetime
    avatar: str

    class Config:
        orm_mode = True


class UserResponse(BaseModel):
    user: UserDb
    detail: str = "User successfully created"


class TokenModel(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class RequestEmail(BaseModel):
    email: EmailStr
