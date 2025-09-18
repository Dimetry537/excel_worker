from pydantic import BaseModel, ConfigDict
from datetime import datetime

class CaxCode(BaseModel):
    cax_name: str
    cax_code: int
    quantity_of_days: int

    model_config = ConfigDict(from_attributes=True)

class CaxCodeCreate(CaxCode):
    pass

class CaxCodeRead(CaxCode):
    id: int
    is_active: bool
    created_at: datetime
    updated_at: datetime
