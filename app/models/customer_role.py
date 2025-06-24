from sqlalchemy import Column, String, ForeignKey,  UUID
from app.models.role import Role

class CustomerRole(Role):
    __tablename__ = "customer_role"

    id = Column(UUID, ForeignKey("role.id"), primary_key=True)
    phone = Column(String, nullable=True)
    address = Column(String, nullable=True)

    __mapper_args__ = {
        "polymorphic_identity": "customer"
    }
