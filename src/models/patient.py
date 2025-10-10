from sqlalchemy import Column, Integer, String, Date, Boolean
from src.db.base import Base, TimestampMixin

class Patient(Base, TimestampMixin):
    __tablename__ = "patients"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, unique=False, nullable=False)
    birth_date = Column(Date, nullable=False)
    address = Column(String, nullable=False)
    workplace = Column(String, nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)
