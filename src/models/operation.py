from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship

from src.db.base import Base, TimestampMixin

class Operation(Base, TimestampMixin):
    __tablename__ = "operations"

    id = Column(Integer, primary_key=True, index=True)
    oper_name = Column(String, unique=False, nullable=False)
    oper_protocol = Column(Text, nullable=False)

    medical_history_id = Column(
        Integer,
        ForeignKey("medical_histories.id", ondelete="CASCADE"),
        nullable=False
    )

    medical_history = relationship("MedicalHistory")
