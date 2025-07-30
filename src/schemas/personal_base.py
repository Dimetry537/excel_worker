from pydantic import BaseModel, ConfigDict
from datetime import datetime


class PersonalBase(BaseModel):
    full_name: str

    model_config = ConfigDict(from_attributes=True)

class personalCreate(PersonalBase):
    pass

class PersonalRead(PersonalBase):
    id: int
    created_at: datetime
    updated_at: datetime
