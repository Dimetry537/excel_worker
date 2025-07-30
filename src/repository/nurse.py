from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional
from src.models.nurse import Nurse
from src.schemas.personal_base import PersonalCreate, PersonalRead
from src.repository.base_repository import BaseRepository
    

class NurseRepository(BaseRepository[Nurse]):
    def __init__(self, session: AsyncSession):
        super().__init__(session, Nurse)

    async def create(self, obj_in: PersonalCreate) -> PersonalRead:
        nurse = await super().create(obj_in.model_dump())
        return PersonalRead.model_validate(nurse)
    
    async def update(self, obj_id: int, obj_in: PersonalCreate) -> Optional[Nurse]:
        nurse = await super().update(obj_id, obj_in.model_dump())
        if nurse:
            return PersonalRead.model_validate(nurse)
        return None
    
    async def delete(self, id: int) -> Optional[PersonalRead]:
        nurse = await super().delete(id)
        if nurse:
            return PersonalRead.model_validate(nurse)
        return None
    
    async def get_all(self) -> list[PersonalRead]:
        nurses = await super().get_all()
        return [PersonalRead.model_validate(nurse) for nurse in nurses]
    
    async def get_by_id(self, id: int) -> Optional[PersonalRead]:
        nurse = await super().get_by_id(id)
        if nurse:
            return PersonalRead.model_validate(nurse)
        return None