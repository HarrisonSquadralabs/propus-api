from sqlalchemy import Column, Integer, String, ForeignKey, Enum
from sqlalchemy.orm import relationship
from app.models.entity import EntityAbstract
from sqlalchemy.dialects.postgresql import UUID
import uuid


class ProjectFile(EntityAbstract):
    __tablename__ = "project_files"
    
    project_id = Column(UUID(as_uuid=True), ForeignKey("projects.id"), nullable=False)
    filename = Column(String, nullable=False)
    original_name = Column(String, nullable=True)
    url = Column(String, nullable=True)

    project = relationship("Project", back_populates="files")