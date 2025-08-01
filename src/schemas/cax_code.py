from pydantic import BaseModel, ConfigDict
from datetime import datetime

class CaxCode(BaseModel):
    cax_name: str
    cax_code: int

    model_config = ConfigDict(from_attributes=True)

class CaxCodeCreate(CaxCode):
    pass

class CaxCodeRead(CaxCode):
    id: int
    created_at: datetime
    updated_at: datetime
