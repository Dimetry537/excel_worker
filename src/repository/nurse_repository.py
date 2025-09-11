from sqlalchemy import select, exists
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional
from fastapi import HTTPException

from src.models.nurse import Nurse
from src.schemas.personal_base import PersonalCreate, PersonalRead
from src.repository.base_repository import BaseRepository
from src.models.medical_hystory import MedicalHistory
    

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
        stmt = select(exists().where(MedicalHistory.nurse_id == id))
        result = await self.session.execute(stmt)
        has_histories = result.scalar()

        nurse = await self.session.get(Nurse, id)
        if not nurse:
            return None
        
        if has_histories:
            nurse.is_active = False
            await self.session.commit()
            await self.session.refresh(nurse)
            
            raise HTTPException(
                status_code=400,
                detail="Медсестра не удалена, так как связана с медицинскими историями. Медсестра переведена в статус 'неактивный'."
            )
        
        await self.session.delete(nurse)
        await self.session.commit()
        return PersonalRead.model_validate(nurse)
    
    async def toggle_active(self, obj_id: int) -> Optional[PersonalRead]:
        nurse = await self.session.get(Nurse, obj_id)
        if not nurse:
            return None

        nurse.is_active = not nurse.is_active
        await self.session.commit()
        await self.session.refresh(nurse)
        return PersonalRead.model_validate(nurse)
