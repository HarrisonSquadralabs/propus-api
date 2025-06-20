# from sqlalchemy import Column, String, Enum, UUID
# from sqlalchemy.orm import relationship
# from app.models.entity import EntityAbstract
# import enum

# class RoleName(str, enum.Enum):
#     architect = "Architect"
#     customer = "Customer"
#     supplier = "Supplier"

# class Role(EntityAbstract):
#     __tablename__ = "role"

#     name = Column(Enum(RoleName), nullable=False)
#     users = relationship("User", back_populates="role")
#     permissions = relationship("Permission", secondary="role_permissions", back_populates="roles")

#     # Inheritance setup
#     type = Column(String(50))
#     __mapper_args__ = {
#         "polymorphic_identity": "role",
#         "polymorphic_on": type
#     }


from sqlalchemy import Column, Integer, Enum, String
from sqlalchemy.orm import relationship
from app.models.entity import EntityAbstract
import enum

class RoleType(str, enum.Enum):
    customer = "customer"
    architect = "architect"
    supplier = "supplier"

class Role(EntityAbstract):
    __tablename__ = "role"

    type = Column(Enum(RoleType), nullable=False)

    users = relationship("User", back_populates="role")

    __mapper_args__ = {
        "polymorphic_identity": "role",
        "polymorphic_on": type
    }
