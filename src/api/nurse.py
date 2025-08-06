from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from src.schemas.personal_base import PersonalCreate, PersonalRead
from src.repository.nurse_repository import NurseRepository
from src.db.base import get_async_session

router = APIRouter(prefix="/nurses", tags=["nurses"])

@router.post("/", response_model=PersonalRead)
async def create_nurse(
    nurse_in: PersonalCreate,
    session: AsyncSession = Depends(get_async_session)
):
    repo = NurseRepository(session)
    nurse = await repo.create(nurse_in)
    return PersonalRead.model_validate(nurse)

@router.get("/", response_model=list[PersonalRead])
async def get_nurses(
    session: AsyncSession = Depends(get_async_session)
):
    repo = NurseRepository(session)
    nurses = await repo.get_all()
    return [PersonalRead.model_validate(nur) for nur in nurses]

@router.get("/{nurse_id}", response_model=PersonalRead)
async def get_nurse_by_id(
    nurse_id: int,
    session: AsyncSession = Depends(get_async_session)
):
    repo = NurseRepository(session)
    nurse = await repo.get_by_id(nurse_id)
    if not nurse:
        raise HTTPException(status_code=404, detail="Nurse not found")
    return PersonalRead.model_validate(nurse)

@router.put("/{nurse_id}", response_model=PersonalRead)
async def update_nurse(
    nurse_id: int,
    nurse_in: PersonalCreate,
    session: AsyncSession = Depends(get_async_session)
):
    repo = NurseRepository(session)
    updated = await repo.update(nurse_id, nurse_in)
    if not updated:
        raise HTTPException(status_code=404, detail="Nurse not found")
    return PersonalRead.model_validate(updated)

@router.delete("/{nurse_id}", response_model=PersonalRead)
async def delete_nurse(
    nurse_id: int,
    session: AsyncSession = Depends(get_async_session)
):
    repo = NurseRepository(session)
    deleted = await repo.delete(nurse_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Nurse not found")
    return PersonalRead.model_validate(deleted)

@router.patch("/{nurse_id}/toggle_active", response_model=PersonalRead)
async def toggle_active_status(
    nurse_id: int,
    session: AsyncSession = Depends(get_async_session)
):
    repo = NurseRepository(session)
    updated = await repo.toggle_active(nurse_id)
    if not updated:
        raise HTTPException(status_code=404, detail="Nurse not found")
    return updated
