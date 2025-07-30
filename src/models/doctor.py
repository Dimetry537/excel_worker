from sqlalchemy import Column, Integer, String
from sqlalchemy.dialects.postgresql import TIMESTAMP
from datetime import datetime, timezone

from src.db.base import Base, TimestampMixin

class Doctor(Base, TimestampMixin):
    __tablename__ = "doctors"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, unique=True, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), default=datetime.now(timezone.utc))
    updated_at = Column(TIMESTAMP(timezone=True), default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))
