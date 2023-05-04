from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import relationship

from database.configuration import Base

class Floor(Base):
    __tablename__ = "floor"

    floor_id = Column(Integer, primary_key=True, index=True)
    floor_name = Column(String(256))
    floor_image = Column(String(256))
    floor_description = Column(String(256))
    floor_price = Column(Float)


class User(Base):
    __tablename__ = 'user'

    user_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(256))
    user_email = Column(String(256))
    user_pass = Column(String(256))


# class Token(BaseModel):
#     access_token: str
#     token_type: str


# class TokenData(BaseModel):
#     user_email: Optional[str] = None

