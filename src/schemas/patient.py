from pydantic import BaseModel, ConfigDict
from datetime import date, datetime
from typing import Optional

class PatientBase(BaseModel):
    full_name: str
    birth_date: date
    adress: str
    workplace: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)

class PatientCreate(PatientBase):
    pass

class PatientRead(PatientBase):
    id: int
    is_active: bool
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
