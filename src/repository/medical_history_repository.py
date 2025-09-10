from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, extract
from typing import Optional
from sqlalchemy.orm import selectinload

from src.models.medical_hystory import MedicalHistory
from src.schemas.medical_history_base import MedicalHistoryCreate, MedicalHistoryRead
from src.repository.base_repository import BaseRepository

class MedicalHistoryRepository(BaseRepository[MedicalHistory]):
    def __init__(self, session: AsyncSession):
        super().__init__(session, MedicalHistory)

    async def get_next_history_number(self, year: int) -> int:
        stmt = select(func.max(MedicalHistory.history_number)).where(
            extract('year', MedicalHistory.admission_date) == year
        )
        result = await self.session.execute(stmt)
        max_number = result.scalar() or 0
        return max_number + 1
    
    async def create(self, obj_in: MedicalHistoryCreate) -> MedicalHistoryRead:
        admission_year = obj_in.admission_date.year
        next_number = await self.get_next_history_number(admission_year)

        obj_data = obj_in.model_dump()
        obj_data["history_number"] = next_number

        created = await super().create(obj_data)
        stmt = (
            select(MedicalHistory)
            .options(
                selectinload(MedicalHistory.doctor),
                selectinload(MedicalHistory.nurse),
                selectinload(MedicalHistory.cax_code),
            )
            .where(MedicalHistory.id == created.id )
        )
        result = await self.session.execute(stmt)
        history = result.scalar_one()
        return MedicalHistoryRead.model_validate(history)
    
    async def update(
            self, obj_id: int, obj_in: MedicalHistoryCreate
    ) -> Optional[MedicalHistoryRead]:
        updated = await super().update(obj_id, obj_in.model_dump())
        if updated:
            stmt = (
                select(MedicalHistory)
                .options(
                    selectinload(MedicalHistory.doctor),
                    selectinload(MedicalHistory.nurse),
                    selectinload(MedicalHistory.cax_code),
                )
                .where(MedicalHistory.id == updated.id)
            )
            result = await self.session.execute(stmt)
            history = result.scalar_one()
            return MedicalHistoryRead.model_validate(history)
        return None
    
    async def get_by_id(self, obj_id: int) -> Optional[MedicalHistoryRead]:
        stmt = (
            select(MedicalHistory)
            .options(
                selectinload(MedicalHistory.doctor),
                selectinload(MedicalHistory.nurse),
                selectinload(MedicalHistory.cax_code),
            )
            .where(MedicalHistory.id == obj_id)
        )
        result = await self.session.execute(stmt)
        history = result.scalar_one_or_none()
        if history:
            return MedicalHistoryRead.model_validate(history)
        return None
    
    async def get_all(self) -> list[MedicalHistoryRead]:
        stmt = (
            select(MedicalHistory)
            .options(
                selectinload(MedicalHistory.doctor),
                selectinload(MedicalHistory.nurse),
                selectinload(MedicalHistory.cax_code),
            )
        )
        result = await self.session.execute(stmt)
        return [MedicalHistoryRead.model_validate(r) for r in result.scalars().all()]
    
    async def get_filltered(self, full_name: Optional[str] = None, admission_date: Optional[str] = None) -> list[MedicalHistoryRead]:
        stmt = select(MedicalHistory).options(
            selectinload(MedicalHistory.doctor),
            selectinload(MedicalHistory.nurse),
            selectinload(MedicalHistory.cax_code),
        )
        if full_name:
            stmt = stmt.where(MedicalHistory.full_name.ilike(f"%{full_name}%"))
        if admission_date:
            stmt = stmt.where(MedicalHistory.admission_date == admission_date)
        result = await self.session.execute(stmt)
        return [MedicalHistoryRead.model_validate(r) for r in result.scalars().all()]
