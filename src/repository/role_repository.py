from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from src.models.role import Role
from src.schemas.auth import RoleCreate, RoleRead
from src.repository.base_repository import BaseRepository

class RoleRepository(BaseRepository[Role]):
    def __init__(self, session: AsyncSession):
        super().__init__(session, Role)

    async def create(self, obj_in: RoleCreate) -> RoleRead:
        role_data = {"name": obj_in.name}
        role = await super().create(role_data)
        return RoleRead.model_validate(role)

    async def get_by_name(self, name: str):
        stmt = select(Role).where(Role.name == name)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()
