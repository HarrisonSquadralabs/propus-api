from sqlalchemy import Column, Enum
from sqlalchemy.orm import relationship
from app.models.entity import EntityAbstract
from app.models.permission import role_permissions
import enum

class RoleType(str, enum.Enum):
    customer = "customer"
    architect = "architect"
    supplier = "supplier"

class Role(EntityAbstract):
    __tablename__ = "role"

    type = Column(Enum(RoleType), nullable=False)

    users = relationship("User", back_populates="role")
    permissions = relationship("Permission", secondary=role_permissions, back_populates="roles")

    __mapper_args__ = {
        "polymorphic_identity": "role",
        "polymorphic_on": type
    }
