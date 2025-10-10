from sqlalchemy import Column
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.doctor import Doctor
from src.models.medical_hystory import MedicalHistory
from src.repository.personal_repository import PersonalRepository

class DoctorRepository(PersonalRepository[Doctor]):
    def __init__(self, session: AsyncSession):
        super().__init__(session, Doctor)
        self.history_link_field = MedicalHistory.doctor_id
        self.entity_name = "Доктор"
