from sqlalchemy import Column, Integer, String

from src.db.base import Base, TimestampMixin

class Nurse(Base, TimestampMixin):
    __tablename__ = "nurses"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, unique=True, nullable=False)
