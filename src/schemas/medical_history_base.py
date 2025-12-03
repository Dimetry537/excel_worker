from pydantic import BaseModel, ConfigDict
from datetime import date, datetime
from typing import Optional

from src.schemas.personal_base import PersonalRead
from src.schemas.cax_code import CaxCodeRead
from src.schemas.patient import PatientRead

class _MedicalHistoryBase(BaseModel):
    admission_date: date
    discharge_date: Optional[date] = None
    diagnosis: str
    icd10_code: str

    cax_code_id: int
    doctor_id: int
    nurse_id: int

    model_config = ConfigDict(from_attributes=True)

class MedicalHistoryCreate(_MedicalHistoryBase):
    full_name: str
    birth_date: date
    address: str
    workplace: Optional[str] = None

class MedicalHistoryUpdate(BaseModel):
    diagnosis: Optional[str] = None
    icd10_code: Optional[str] = None
    cax_code_id: Optional[int] = None
    doctor_id: Optional[int] = None
    nurse_id: Optional[int] = None
    discharge_date: Optional[date] = None

    model_config = ConfigDict(from_attributes=True)

class MedicalHistoryRead(_MedicalHistoryBase):
    id: int
    history_number: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    cancelled: Optional[str] = None

    patient: PatientRead
    doctor: PersonalRead
    nurse: PersonalRead
    cax_code: CaxCodeRead
