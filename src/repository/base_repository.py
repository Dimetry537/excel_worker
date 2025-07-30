from typing import Type, TypeVar, Generic, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

T = TypeVar('T')

class BaseRepository(Generic[T]):
    def __init__(self, session: AsyncSession, model: Type[T]):
        self.session = session
        self.model = model

    async def get_by_id(self, id: int) -> T | None:
        stmt = select(self.model).where(self.model.id == id)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()
    
    async def get_all(self) -> list[T]:
        stmt = select(self.model)
        result = await self.session.execute(stmt)
        return result.scalars().all()
    
    async def create(self, obj_in: dict) -> T:
        obj = self.model(**obj_in)
        self.session.add(obj)
        await self.session.commit()
        await self.session.refresh(obj)
        return obj
    
    async def update(self, obj_id: int, obj_in: dict) -> T | None:
        obj = await self.get_by_id(obj_id)

        if not obj:
            return None
        for key, value in obj_in.items():
            setattr(obj, key, value)

        await self.session.commit()
        await self.session.refresh(obj)
        return obj
    
    async def delete(self, obj_id: int) -> Optional[T]:
        obj = await self.get_by_id(obj_id)
        if obj is None:
            return None
        await self.session.delete(obj)
        await self.session.commit()
        return obj
