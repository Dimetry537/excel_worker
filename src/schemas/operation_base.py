from datetime import datetime
from pydantic import BaseModel, ConfigDict

class OperationBase(BaseModel):
    oper_name: str
    oper_protocol: str | None = None
    medical_history_id: int

    model_config = ConfigDict(from_attributes=True)

class OperationCreate(OperationBase):
    pass

class OperationRead(OperationBase):
    id: int
    created_at: datetime
    updated_at: datetime
