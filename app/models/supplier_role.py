from sqlalchemy import Column, String, ForeignKey, UUID
from app.models.role import Role

class SupplierRole(Role):
    __tablename__ = "supplier_role"

    id = Column(UUID, ForeignKey("role.id"), primary_key=True)
    phone = Column(String, nullable=False)
    company = Column(String, nullable=False)
    address = Column(String, nullable=False)

    __mapper_args__ = {
        "polymorphic_identity": "supplier"
    }
