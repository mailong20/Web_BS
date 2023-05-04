from typing import List, Optional

from pydantic import BaseModel


class FloorBase(BaseModel):
    floor_name: str
    floor_image: str
    floor_image: str
    floor_description: str
    floor_price: str

class Floor(FloorBase):
    class Config:
        orm_mode = True

class User(BaseModel):
    name: str
    user_email: str
    user_pass: str

class ShowUser(BaseModel):
    name: str
    user_email: str

    class Config:
        orm_mode = True

class ShowFloor(BaseModel):
    floor_name: str
    floor_image: str
    floor_image: str
    floor_description: str
    floor_price: str
    class Config:
        orm_mode = True

class Login(BaseModel):
    username: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None