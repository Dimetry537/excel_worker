from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional
from src.models.doctor import Doctor
from src.schemas.personal_base import PersonalCreate, PersonalRead
from src.repository.base_repository import BaseRepository

class DoctorRepository(BaseRepository[Doctor]):
    def __init__(self, session: AsyncSession):
        super().__init__(session, Doctor)

    async def create(self, obj_in: PersonalCreate) -> PersonalRead:
        doctor = await super().create(obj_in.model_dump())
        return PersonalRead.model_validate(doctor)
    
    async def update(self, obj_id: int, obj_in: PersonalCreate) -> Optional[PersonalRead]:
        updated = await super().update(obj_id, obj_in.model_dump())
        if updated:
            return PersonalRead.model_validate(updated)
        return None

    async def delete(self, id: int) -> Optional[PersonalRead]:
        doctor = await super().delete(id)
        if doctor:
            return PersonalRead.model_validate(doctor)
        return None
