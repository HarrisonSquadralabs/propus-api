from sqlalchemy import Table, Column, ForeignKey, UUID, String
from app.core.database import Base  # Asegúrate que sea tu Base declarativa
from app.models.entity import EntityAbstract
from sqlalchemy.orm import relationship
# Tabla intermedia muchos a muchos
role_permissions = Table(
    "role_permissions",
    Base.metadata,
    Column("role_id", UUID, ForeignKey("role.id")),
    Column("permission_id", UUID, ForeignKey("permission.id"))
)
class Permission(EntityAbstract):
    __tablename__ = "permission"

    name = Column(String, nullable=False)
    description = Column(String, nullable=True)

    roles = relationship("Role", secondary=role_permissions, back_populates="permissions")  