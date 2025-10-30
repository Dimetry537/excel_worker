from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, extract, update
from typing import Optional
from sqlalchemy.orm import selectinload
from datetime import datetime

from src.models.medical_hystory import MedicalHistory
from src.schemas.medical_history_base import MedicalHistoryCreate, MedicalHistoryRead
from src.repository.base_repository import BaseRepository
from src.repository.patient_repository import PatientRepository
from src.models.patient import Patient
from src.schemas.patient import PatientCreate

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
        patient_repo = PatientRepository(self.session)
        
        stmt = select(Patient).where(
            Patient.full_name == obj_in.full_name,
            Patient.birth_date == obj_in.birth_date,
            Patient.address == obj_in.address
        )
        result = await self.session.execute(stmt)
        patient = result.scalar_one_or_none()
        
        if not patient:
            patient_data = PatientCreate(
                full_name=obj_in.full_name,
                birth_date=obj_in.birth_date,
                address=obj_in.address,
                workplace=None
            )
            patient = await patient_repo.create(patient_data)

        admission_year = obj_in.admission_date.year
        next_number = await self.get_next_history_number(admission_year)

        obj_data = {
            "history_number": next_number,
            "admission_date": obj_in.admission_date,
            "discharge_date": obj_in.discharge_date,
            "diagnosis": obj_in.diagnosis,
            "icd10_code": obj_in.icd10_code,
            "patient_id": patient.id,
            "cax_code_id": obj_in.cax_code_id,
            "doctor_id": obj_in.doctor_id,
            "nurse_id": obj_in.nurse_id,
        }

        created = await super().create(obj_data)
        
        stmt = (
            select(MedicalHistory)
            .options(
                selectinload(MedicalHistory.patient),
                selectinload(MedicalHistory.doctor),
                selectinload(MedicalHistory.nurse),
                selectinload(MedicalHistory.cax_code),
            )
            .where(MedicalHistory.id == created.id)
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
                    selectinload(MedicalHistory.patient),
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
                selectinload(MedicalHistory.patient),
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
                selectinload(MedicalHistory.patient),
                selectinload(MedicalHistory.doctor),
                selectinload(MedicalHistory.nurse),
                selectinload(MedicalHistory.cax_code),
            )
        )
        result = await self.session.execute(stmt)
        return [MedicalHistoryRead.model_validate(r) for r in result.scalars().all()]
    
    async def get_filtered(self, full_name: Optional[str] = None, start_date: Optional[str] = None, end_date: Optional[str] = None) -> list[MedicalHistoryRead]:
        stmt = select(MedicalHistory).options(
            selectinload(MedicalHistory.patient),
            selectinload(MedicalHistory.doctor),
            selectinload(MedicalHistory.nurse),
            selectinload(MedicalHistory.cax_code),
        )
        if full_name:
            stmt = stmt.where(MedicalHistory.full_name.ilike(f"%{full_name}%"))
        
        parsed_start_date = None
        if start_date:
            try:
                parsed_start_date = datetime.strptime(start_date, '%d.%m.%Y').date()
            except ValueError:
                try:
                    parsed_start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
                except ValueError:
                    raise ValueError(f"Неверный формат start_date: {start_date}. Ожидается DD.MM.YYYY или YYYY-MM-DD")
            stmt = stmt.where(MedicalHistory.admission_date >= parsed_start_date)
        
        parsed_end_date = None
        if end_date:
            try:
                parsed_end_date = datetime.strptime(end_date, '%d.%m.%Y').date()
            except ValueError:
                try:
                    parsed_end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
                except ValueError:
                    raise ValueError(f"Неверный формат end_date: {end_date}. Ожидается DD.MM.YYYY или YYYY-MM-DD")
            stmt = stmt.where(MedicalHistory.admission_date <= parsed_end_date)
        
        result = await self.session.execute(stmt)
        return [MedicalHistoryRead.model_validate(r) for r in result.scalars().all()]

    async def cancel(self, obj_id: int) -> Optional[MedicalHistoryRead]:
        stmt = (
            update(MedicalHistory)
            .where(MedicalHistory.id == obj_id)
            .values(cancelled="отменена")
            .returning(MedicalHistory)
        )
        result = await self.session.execute(stmt)
        await self.session.commit()
        history = result.scalar_one_or_none()
        if history:
            stmt = (
                select(MedicalHistory)
                .options(
                    selectinload(MedicalHistory.patient),
                    selectinload(MedicalHistory.doctor),
                    selectinload(MedicalHistory.nurse),
                    selectinload(MedicalHistory.cax_code),
                )
                .where(MedicalHistory.id == obj_id)
            )
            result = await self.session.execute(stmt)
            history = result.scalar_one()
            return MedicalHistoryRead.model_validate(history)
        return None

    async def reactivate(self, obj_id: int) -> Optional[MedicalHistoryRead]:
        stmt = (
            update(MedicalHistory)
            .where(MedicalHistory.id == obj_id)
            .values(cancelled=None)
            .returning(MedicalHistory)
        )
        result = await self.session.execute(stmt)
        await self.session.commit()
        history = result.scalar_one_or_none()
        if history:
            stmt = (
                select(MedicalHistory)
                .options(
                    selectinload(MedicalHistory.patient),
                    selectinload(MedicalHistory.doctor),
                    selectinload(MedicalHistory.nurse),
                    selectinload(MedicalHistory.cax_code),
                )
                .where(MedicalHistory.id == obj_id)
            )
            result = await self.session.execute(stmt)
            history = result.scalar_one()
            return MedicalHistoryRead.model_validate(history)
        return None
