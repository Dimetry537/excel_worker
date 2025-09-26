from sqlalchemy import Column, Integer, String, Date, ForeignKey, UniqueConstraint, extract
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import TIMESTAMP
from datetime import datetime, timezone

from src.db.base import Base, TimestampMixin
from src.models.cax_code import CaxCode
from src.models.doctor import Doctor
from src.models.nurse import Nurse

class MedicalHistory(Base, TimestampMixin):
    __tablename__ = "medical_histories"
    __table_args__ = (
        UniqueConstraint('history_number', 'admission_date', name='uq_history_number_admission_date'),
    )

    id = Column(Integer, primary_key=True, index=True)
    history_number = Column(Integer, unique=False, nullable=False)
    admission_date = Column(Date, nullable=False)
    discharge_date = Column(Date)
    full_name = Column(String, nullable=False)
    birth_date = Column(Date, nullable=False)
    address = Column(String, nullable=False)
    diagnosis = Column(String, nullable=False)
    icd10_code = Column(String, nullable=False)
    cancelled = Column(String, nullable=True)

    cax_code_id = Column(Integer, ForeignKey("cax_codes.id"), nullable=False)
    doctor_id = Column(Integer, ForeignKey("doctors.id"), nullable=False)
    nurse_id = Column(Integer, ForeignKey("nurses.id"), nullable=False)

    cax_code = relationship("CaxCode")
    doctor = relationship("Doctor")
    nurse = relationship("Nurse")
    