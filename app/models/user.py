from sqlalchemy import Column, String, Boolean, ForeignKey, UUID
from sqlalchemy.orm import relationship
from app.models.entity import EntityAbstract

class User(EntityAbstract):
    __tablename__ = "user"

    email = Column(String, unique=True, nullable=False)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    hashed_password = Column(String, nullable=True)
    is_completed = Column(Boolean, default=False)

    role_id = Column(UUID, ForeignKey("role.id"))
    role = relationship("Role", back_populates="users")
