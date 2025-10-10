from sqlalchemy import Column
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.nurse import Nurse
from src.models.medical_hystory import MedicalHistory
from src.repository.personal_repository import PersonalRepository

class NurseRepository(PersonalRepository[Nurse]):
    def __init__(self, session: AsyncSession):
        super().__init__(session, Nurse)
        self.history_link_field = MedicalHistory.nurse_id
        self.entity_name = "Медсестра"
