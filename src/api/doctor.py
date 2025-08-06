from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from src.schemas.personal_base import PersonalCreate, PersonalRead
from src.repository.doctor_repository import DoctorRepository
from src.db.base import get_async_session

router = APIRouter(prefix="/doctors", tags=["doctors"])

@router.post("/", response_model=PersonalRead)
async def create_doctor(
    doctor_in: PersonalCreate,
    session: AsyncSession = Depends(get_async_session)
):
    repo = DoctorRepository(session)
    doctor = await repo.create(doctor_in)
    return PersonalRead.model_validate(doctor)

@router.get("/", response_model=list[PersonalRead])
async def get_doctors(
    session: AsyncSession = Depends(get_async_session)
):
    repo = DoctorRepository(session)
    doctors = await repo.get_all()
    return [PersonalRead.model_validate(doc) for doc in doctors]

@router.get("/{doctor_id}", response_model=PersonalRead)
async def get_doctor_by_id(
    doctor_id: int,
    session: AsyncSession = Depends(get_async_session)
):
    repo = DoctorRepository(session)
    doctor = await repo.get_by_id(doctor_id)
    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")
    return PersonalRead.model_validate(doctor)

@router.put("/{doctor_id}", response_model=PersonalRead)
async def update_doctor(
    doctor_id: int,
    doctor_in: PersonalCreate,
    session: AsyncSession = Depends(get_async_session)
):
    repo = DoctorRepository(session)
    updated = await repo.update(doctor_id, doctor_in)
    if not updated:
        raise HTTPException(status_code=404, detail="Doctor not found")
    return PersonalRead.model_validate(updated)

@router.delete("/{doctor_id}", response_model=PersonalRead)
async def delete_doctor(
    doctor_id: int,
    session: AsyncSession = Depends(get_async_session)
):
    repo = DoctorRepository(session)
    deleted = await repo.delete(doctor_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Doctor not found")
    return PersonalRead.model_validate(deleted)

@router.patch("/{doctor_id}/toggle_active", response_model=PersonalRead)
async def toggle_active_status(
    doctor_id: int,
    session: AsyncSession = Depends(get_async_session)
):
    repo = DoctorRepository(session)
    updated = await repo.toggle_active(doctor_id)
    if not updated:
        raise HTTPException(status_code=404, detail="Doctor not found")
    return updated

