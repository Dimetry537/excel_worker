from sqlalchemy import Column, Integer, String
from sqlalchemy.dialects.postgresql import TIMESTAMP
from datetime import datetime, timezone

from src.db.base import Base, TimestampMixin

class CaxCode(Base, TimestampMixin):
    __tablename__ = "cax_codes"

    id = Column(Integer, primary_key=True, index=True)
    cax_name = Column(String, unique=True, nullable=False)
    cax_code = Column(Integer, unique=True, nullable=False)
    quantity_of_days = Column(Integer, unique=False, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), default=datetime.now(timezone.utc))
    updated_at = Column(TIMESTAMP(timezone=True), default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))
