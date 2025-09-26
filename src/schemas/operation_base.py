from datetime import datetime
from pydantic import BaseModel

class OperationBase(BaseModel):
    oper_name: str
    oper_protocol: str
    medical_history_id: int

class OperationCreate(OperationBase):
    pass


class OperationUpdate(BaseModel):
    oper_name: str | None = None
    oper_protocol: str | None = None
    medical_history_id: int | None = None


class OperationRead(OperationBase):
    id: int
    created_at: datetime | None = None
    updated_at: datetime | None = None

    class Config:
        from_attributes = True
