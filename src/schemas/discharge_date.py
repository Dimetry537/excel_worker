from pydantic import BaseModel
from datetime import date

class DischargeDateRequest(BaseModel):
    admission_date: date
    cax_code_id: int


class DischargeDateResponse(BaseModel):
    discharge_date: date
