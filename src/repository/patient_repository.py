from sqlalchemy import select, exists
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional
from fastapi import HTTPException

from src.models.patient import Patient
from src.schemas.patient import PatientCreate, PatientRead
from src.repository.base_repository import BaseRepository
from src.models.medical_hystory import MedicalHistory

class PatientRepository(BaseRepository[Patient]):
    def __init__(self, session: AsyncSession):
        super().__init__(session, Patient)

    async def create(self, obj_in: PatientCreate) -> PatientRead:
        patient = await super().create(obj_in.model_dump())
        return PatientRead.model_validate(patient)
    
    async def update(self, obj_id: int, obj_in: PatientCreate) -> Optional[PatientRead]:
        updated = await super().update(obj_id, obj_in.model_dump())
        if updated:
            return PatientRead.model_validate(updated)
        return None
    
    async def delete(self, id: int) -> Optional[PatientRead]:
        stmt = select(exists().where(MedicalHistory.patient_id == id))
        result = await self.session.execute(stmt)
        has_histories = result.scalar()

        patient = await self.session.get(Patient, id)
        if not patient:
            return None
        
        if has_histories:
            patient.is_active = False
            await self.session.commit()
            await self.session.refresh(patient)
            
            raise HTTPException(
                status_code=400,
                detail="Пациент не удален, так как связан с медицинскими историями. Пациент переведен в статус 'неактивный'."
            )
        
        await self.session.delete(patient)
        await self.session.commit()
        return PatientRead.model_validate(patient)
    
    async def toggle_active(self, obj_id: int) -> Optional[PatientRead]:
        patient = await self.session.get(Patient, obj_id)
        if not patient:
            return None

        patient.is_active = not patient.is_active
        await self.session.commit()
        await self.session.refresh(patient)
        return PatientRead.model_validate(patient)
