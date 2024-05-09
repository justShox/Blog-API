from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional


class Post(BaseModel):
    title: str
    content: str
    published: bool


class UpdatePost(BaseModel):
    title: str
    content: str


class PostResponse(Post):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True


class CreateUser(BaseModel):
    e_mail: EmailStr
    password: str

    class Config:
        orm_mode = True


class GetUser(BaseModel):
    id: int
    e_mail: EmailStr
    created_at: datetime

    class Config:
        orm_mode = True


class UserLogin(BaseModel):
    e_mail: EmailStr
    password: str

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[str] = None
