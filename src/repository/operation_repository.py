from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional

from src.models.operation import Operation
from src.schemas.operation_base import OperationCreate, OperationRead, OperationUpdate
from src.repository.base_repository import BaseRepository


class OperationRepository(BaseRepository[Operation]):
    def __init__(self, session: AsyncSession):
        super().__init__(session, Operation)

    async def create(self, obj_in: OperationCreate) -> OperationRead:
        operation = await super().create(obj_in.model_dump())
        return OperationRead.model_validate(operation)

    async def update(self, obj_id: int, obj_in: OperationUpdate | dict) -> Optional[OperationRead]:
        data = obj_in if isinstance(obj_in, dict) else obj_in.model_dump(exclude_unset=True)
        updated = await super().update(obj_id, data)
        if updated:
            return OperationRead.model_validate(updated)
        return None

    async def delete(self, obj_id: int) -> Optional[OperationRead]:
        operation = await super().delete(obj_id)
        if operation:
            return OperationRead.model_validate(operation)
        return None

    async def get_by_id(self, obj_id: int) -> Optional[OperationRead]:
        operation = await super().get_by_id(obj_id)
        if operation:
            return OperationRead.model_validate(operation)
        return None
