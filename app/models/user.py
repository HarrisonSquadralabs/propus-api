# from sqlalchemy import Column, String, Boolean, ForeignKey, UUID
# from sqlalchemy.orm import relationship
# from app.models.entity import EntityAbstract

# class User(EntityAbstract):
#     __tablename__ = "user"

#     email = Column(String, unique=True, index=True, nullable=False)
#     first_name = Column(String, nullable=False)
#     last_name = Column(String, nullable=False)
#     hashed_password = Column(String, nullable=True)
#     role_id = Column(UUID, ForeignKey("role.id"), nullable=True)

#     role = relationship("Role", back_populates="users")
#     is_completed = Column(Boolean, default=False)

#     @property
#     def is_active(self):
#         return not self.disabled


from sqlalchemy import Column, String, Boolean, ForeignKey, Integer
from sqlalchemy.orm import relationship
from app.models.entity import EntityAbstract

class User(EntityAbstract):
    __tablename__ = "user"

    email = Column(String, unique=True, nullable=False)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    hashed_password = Column(String, nullable=True)

    # FK hacia la tabla base 'role'
    role_id = Column(Integer, ForeignKey("role.id"))
    role = relationship("Role", back_populates="users")

    is_completed = Column(Boolean, default=False)
