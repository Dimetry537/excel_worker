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
        updated = await super().update(obj_id, obj_in.model_dump())
        if updated:
            return PersonalRead.model_validate(updated)
        return None
    
    async def delete(self, id: int) -> Optional[PersonalRead]:
        nurse = await super().delete(id)
        if nurse:
            return PersonalRead.model_validate(nurse)
        return None
    
    async def toggle_active(self, obj_id: int) -> Optional[PersonalRead]:
        nurse = await self.session.get(Nurse, obj_id)
        if not nurse:
            return None

        nurse.is_active = not nurse.is_active
        await self.session.commit()
        await self.session.refresh(nurse)
        return PersonalRead.model_validate(nurse)
