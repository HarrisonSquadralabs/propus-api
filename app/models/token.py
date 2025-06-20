from sqlalchemy import Column, String
from app.models.entity import EntityAbstract
from sqlalchemy import Column, String, Integer, ForeignKey


class Token(EntityAbstract):
    __tablename__ = "tokens"
    access_token = Column(String, nullable=False)
    token_type = Column(String, default="bearer")
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False) 

from pydantic import BaseModel

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"