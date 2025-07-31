from pydantic import BaseModel, ConfigDict
from datetime import date, datetime
from typing import Optional

class MedicalHistoryBase(BaseModel):
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

    model_config = ConfigDict(from_attributes=True)

class MedicalHistoryCreate(MedicalHistoryBase):
    pass

class MedicalHistoryRead(MedicalHistoryBase):
    id: int
    history_number: int
    cancelled: Optional[str] = None
    created_at: datetime
    updated_at: datetime
