from sqlalchemy import Column, Integer, String, Float, Enum as SqlEnum, ForeignKey
from sqlalchemy.orm import relationship
from app.schemas.enum import ProjectType, Currency, ProjectStatus
from app.models.entity import EntityAbstract

class Project(EntityAbstract):
    __tablename__ = "projects"

    name = Column(String, nullable=False)
    client_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    architect_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    project_type = Column(SqlEnum(ProjectType), nullable=False)
    currency = Column(SqlEnum(Currency), nullable=False)
    budget = Column(Float, nullable=False)
    location = Column(String, nullable=False)
    status = Column(SqlEnum(ProjectStatus), default=ProjectStatus.in_progress)

    client = relationship("User", foreign_keys=[client_id])
    architect = relationship("User", foreign_keys=[architect_id])
    files = relationship("ProjectFile", back_populates="project", cascade="all, delete-orphan")