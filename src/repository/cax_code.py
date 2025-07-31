from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional

from src.models.cax_code import CaxCode
from src.schemas.cax_code import CaxCodeCreate, CaxCodeRead
from src.repository.base_repository import BaseRepository

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
        deleted = await super().delete(obj_id)
        if deleted:
            return CaxCodeRead.model_validate(deleted)
        return None
    