from sqlalchemy import Column, String, Integer, ForeignKey
from app.models.entity import EntityAbstract

class ArchitectRole(EntityAbstract):
    __tablename__ = "architect_role"

    id = Column(Integer, ForeignKey("role.id"), primary_key=True)
    license_number = Column(String, nullable=True)
    firm_name = Column(String, nullable=True)

    __mapper_args__ = {
        "polymorphic_identity": "architect"
    }
