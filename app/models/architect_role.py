from sqlalchemy import Column, String, ForeignKey, UUID
from app.models.role import Role

class ArchitectRole(Role):
    __tablename__ = "architect_role"

    id = Column(UUID, ForeignKey("role.id"), primary_key=True)
    entity_type = Column(String, nullable=True)

    __mapper_args__ = {
        "polymorphic_identity": "architect"
    }
