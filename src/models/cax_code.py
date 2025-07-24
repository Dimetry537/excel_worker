from sqlalchemy import Column, Integer

from src.db.base import Base, TimestampMixin

class CaxCode(Base, TimestampMixin):
    __tablename__ = "cax_codes"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(Integer, unique=True, nullable=False)
