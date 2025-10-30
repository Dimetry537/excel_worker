from pydantic import BaseModel, ConfigDict
from datetime import date, datetime
from typing import Optional

from src.schemas.personal_base import PersonalRead
from src.schemas.cax_code import CaxCodeRead
from src.schemas.patient import PatientRead

class MedicalHistoryBase(BaseModel):
    admission_date: date
    discharge_date: Optional[date] = None
    diagnosis: str
    icd10_code: str

    cax_code_id: int
    doctor_id: int
    nurse_id: int

    model_config = ConfigDict(from_attributes=True)

class MedicalHistoryCreate(BaseModel):
    admission_date: date
    discharge_date: Optional[date] = None
    full_name: str
    birth_date: date
    address: str
    diagnosis: str
    icd10_code: str
    cax_code_id: int
    doctor_id: int
    nurse_id: int

class MedicalHistoryRead(MedicalHistoryBase):
    id: int
    history_number: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    cancelled: Optional[str] = None

    patient: PatientRead
    doctor: PersonalRead
    nurse: PersonalRead
    cax_code: CaxCodeRead
