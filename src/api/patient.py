from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from src.schemas.patient import PatientCreate, PatientRead
from src.repository.patient_repository import PatientRepository
from src.db.base import get_async_session
from src.auth.dependencies import get_current_user

router = APIRouter(
    prefix="/patients",
    tags=["patients"],
    dependencies=[Depends(get_current_user)]
)

@router.post("/", response_model=PatientRead)
async def create_patient(
    patient_in: PatientCreate,
    session: AsyncSession = Depends(get_async_session)
):
    repo = PatientRepository(session)
    patient = await repo.create(patient_in)
    return PatientRead.model_validate(patient)

@router.get("/", response_model=list[PatientRead])
async def get_patients(
    session: AsyncSession = Depends(get_async_session)
):
    repo = PatientRepository(session)
    patients = await repo.get_all()
    return [PatientRead.model_validate(pat) for pat in patients]

@router.get("/{patient_id}", response_model=PatientRead)
async def get_patient_by_id(
    patient_id: int,
    session: AsyncSession = Depends(get_async_session)
):
    repo = PatientRepository(session)
    patient = await repo.get_by_id(patient_id)
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    return PatientRead.model_validate(patient)

@router.put("/{patient_id}", response_model=PatientRead)
async def update_patient(
    patient_id: int,
    patient_in: PatientCreate,
    session: AsyncSession = Depends(get_async_session)
):
    repo = PatientRepository(session)
    updated = await repo.update(patient_id, patient_in)
    if not updated:
        raise HTTPException(status_code=404, detail="Patient not found")
    return PatientRead.model_validate(updated)

@router.delete("/{patient_id}", response_model=PatientRead)
async def delete_patient(
    patient_id: int,
    session: AsyncSession = Depends(get_async_session)
):
    repo = PatientRepository(session)
    deleted = await repo.delete(patient_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Patient not found")
    return PatientRead.model_validate(deleted)

@router.patch("/{patient_id}/toggle_active", response_model=PatientRead)
async def toggle_active_status(
    patient_id: int,
    session: AsyncSession = Depends(get_async_session)
):
    repo = PatientRepository(session)
    updated = await repo.toggle_active(patient_id)
    if not updated:
        raise HTTPException(status_code=404, detail="Patient not found")
    return updated