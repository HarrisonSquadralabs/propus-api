from app.core.database import Base  # Import your Base defined with declarative_base
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy import Column, UUID, DateTime, Boolean, func
import uuid
from sqlalchemy.dialects.postgresql import UUID
class EntityAbstract(Base):
    __abstract__ = True

    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    create_date = Column(DateTime(timezone=True), server_default=func.now())
    update_date = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    delete_date = Column(DateTime(timezone=True), nullable=True)
    is_deleted = Column(Boolean, default=False)
    disabled = Column(Boolean, default=False)  