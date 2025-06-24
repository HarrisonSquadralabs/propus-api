from sqlalchemy import Column, String
from app.models.entity import EntityAbstract
from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
import uuid

class Token(EntityAbstract):
    __tablename__ = "tokens"
    access_token = Column(String, nullable=False)
    token_type = Column(String, default="bearer")
    user_id = Column(UUID(as_uuid=True), ForeignKey("user.id"), nullable=False)

from pydantic import BaseModel

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"