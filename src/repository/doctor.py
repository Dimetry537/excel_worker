from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional
from src.models.doctor import Doctor
from src.schemas.personal_base import PersonalCreate, PersonalRead
from src.repository.base_repository import BaseRepository

class DoctorRepository(BaseRepository[Doctor]):
    def __init__(self, session: AsyncSession):
        super().__init__(session, Doctor)

    async def create(self, obj_in: PersonalCreate) -> Doctor:
        return await super().create(obj_in.model_dump())
    
    async def update(self, obj_id: int, obj_in: PersonalCreate) -> Optional[Doctor]:
        return await super().update(obj_id, obj_in.model_dump())
    
    async def get_all(self) -> list[PersonalRead]:
        doctors = await super().get_all()
        return [PersonalRead.model_validate(doctor) for doctor in doctors]
    
    async def get_by_id(self, id: int) -> Optional[PersonalRead]:
        doctor = await super().get_by_id(id)
        if doctor:
            return PersonalRead.model_validate(doctor)
        return None

