from sqlalchemy import Column, Integer

from src.db.base import Base, TimestampMixin

class CaxCode(Base, TimestampMixin):
    __tablename__ = "cax_codes"

    id = Column(Integer, primary_key=True, index=True)
    cax_name = Column(Integer, unique=True, nullable=False)
    cax_code = Column(Integer, unique=True, nullable=False)
