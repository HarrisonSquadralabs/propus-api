from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base
from app.models.entity import EntityAbstract

class SupplierRol(EntityAbstract):
    __tablename__ = "supplier_info"

    user_id = Column(Integer, ForeignKey("user.id"), nullable=False, unique=True) 
    phone = Column(String, nullable=False)
    company = Column(String, nullable=False)
    address = Column(String, nullable=False)
    user = relationship("User", back_populates="supplier_info")