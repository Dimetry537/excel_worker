from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship

from src.db.base import Base, TimestampMixin

class User(Base, TimestampMixin):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)

    roles = relationship("Role", secondary="user_roles", back_populates="users")

