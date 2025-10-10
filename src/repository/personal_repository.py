from sqlalchemy import select, exists
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional, Type, TypeVar
from fastapi import HTTPException

from src.models.medical_hystory import MedicalHistory
from src.schemas.personal_base import PersonalCreate, PersonalRead
from src.repository.base_repository import BaseRepository

T = TypeVar('T')

class PersonalRepository(BaseRepository[T]):
    def __init__(self, session: AsyncSession, model: Type[T]):
        super().__init__(session, model)
        self.history_link_field = None
        self.entity_name = "Персонал"

    async def create(self, obj_in: PersonalCreate) -> PersonalRead:
        obj = await super().create(obj_in.model_dump())
        return PersonalRead.model_validate(obj)
    
    async def update(self, obj_id: int, obj_in: PersonalCreate) -> Optional[PersonalRead]:
        updated = await super().update(obj_id, obj_in.model_dump())
        if updated:
            return PersonalRead.model_validate(updated)
        return None

    async def delete(self, id: int) -> Optional[PersonalRead]:
        if self.history_link_field is None:
            raise ValueError("history_link_field must be set in subclass")

        stmt = select(exists().where(self.history_link_field == id))
        result = await self.session.execute(stmt)
        has_histories = result.scalar()

        obj = await self.session.get(self.model, id)
        if not obj:
            return None
        
        if has_histories:
            obj.is_active = False
            await self.session.commit()
            await self.session.refresh(obj)
            
            raise HTTPException(
                status_code=400,
                detail=f"{self.entity_name} не удален, так как связан с медицинскими историями. {self.entity_name} переведен в статус 'неактивный'."
            )
        
        await self.session.delete(obj)
        await self.session.commit()
        return PersonalRead.model_validate(obj)
    
    async def toggle_active(self, obj_id: int) -> Optional[PersonalRead]:
        obj = await self.session.get(self.model, obj_id)
        if not obj:
            return None

        obj.is_active = not obj.is_active
        await self.session.commit()
        await self.session.refresh(obj)
        return PersonalRead.model_validate(obj)
