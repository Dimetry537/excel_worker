from sqlalchemy import select, exists
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional
from fastapi import HTTPException

from src.models.doctor import Doctor
from src.models.medical_hystory import MedicalHistory
from src.schemas.personal_base import PersonalCreate, PersonalRead
from src.repository.base_repository import BaseRepository

class DoctorRepository(BaseRepository[Doctor]):
    def __init__(self, session: AsyncSession):
        super().__init__(session, Doctor)

    async def create(self, obj_in: PersonalCreate) -> PersonalRead:
        doctor = await super().create(obj_in.model_dump())
        return PersonalRead.model_validate(doctor)
    
    async def update(self, obj_id: int, obj_in: PersonalCreate) -> Optional[PersonalRead]:
        updated = await super().update(obj_id, obj_in.model_dump())
        if updated:
            return PersonalRead.model_validate(updated)
        return None

    async def delete(self, id: int) -> Optional[PersonalRead]:
        stmt = select(exists().where(MedicalHistory.doctor_id == id))
        result = await self.session.execute(stmt)
        has_histories = result.scalar()

        doctor = await self.session.get(Doctor, id)
        if not doctor:
            return None
        
        if has_histories:
            doctor.is_active = False
            await self.session.commit()
            await self.session.refresh(doctor)

            raise HTTPException(
                status_code=400,
                detail="Доктор не удален, так как связан с медицинскими историями. Доктор переведен в статус 'неактивный'."
            )
        
        await self.session.delete(doctor)
        await self.session.commit()
        return PersonalRead.model_validate(doctor)
    
    async def toggle_active(self, obj_id: int) -> Optional[PersonalRead]:
        doctor = await self.session.get(Doctor, obj_id)
        if not doctor:
            return None

        doctor.is_active = not doctor.is_active
        await self.session.commit()
        await self.session.refresh(doctor)
        return PersonalRead.model_validate(doctor)

