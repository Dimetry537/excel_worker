from sqlalchemy import select, exists
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional
from fastapi import HTTPException

from src.models.cax_code import CaxCode
from src.schemas.cax_code import CaxCodeCreate, CaxCodeRead
from src.repository.base_repository import BaseRepository
from src.models.medical_hystory import MedicalHistory

class CaxCodeRepository(BaseRepository[CaxCode]):
    def __init__(self, session: AsyncSession):
        super().__init__(session, CaxCode)

    async def create(self, obj_in: CaxCodeCreate) -> CaxCodeRead:
        crerated = await super().create(obj_in.model_dump())
        return CaxCodeRead.model_validate(crerated)
    
    async def update(self, obj_id: int, obj_in: CaxCodeCreate) -> Optional[CaxCodeRead]:
        updated = await super().update(obj_id, obj_in.model_dump())
        if updated:
            return CaxCodeRead.model_validate(updated)
        return None
    
    async def delete(self, obj_id: int) -> Optional[CaxCodeRead]:
        stmt = select(exists().where(MedicalHistory.cax_code_id == obj_id))
        result = await self.session.execute(stmt)
        has_histories = result.scalar()
        cax_code = await self.session.get(CaxCode, obj_id)
        if not cax_code:
            return None
        
        if has_histories:
            cax_code.is_active = False
            await self.session.commit()
            await self.session.refresh(cax_code)

            raise HTTPException(
                status_code=400,
                detail="Код не удален, так как связан с медицинскими историями. Код переведен в статус 'неактивный'."
            )
        
        await self.session.delete(cax_code)
        await self.session.commit()
        return CaxCodeRead.model_validate(cax_code)
    
    async def toggle_active(self, obj_id: int) -> Optional[CaxCodeRead]:
        cax_code = await self.session.get(CaxCode, obj_id)
        if not cax_code:
            return None

        cax_code.is_active = not cax_code.is_active
        await self.session.commit()
        await self.session.refresh(cax_code)
        return CaxCodeRead.model_validate(cax_code)
    