from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional

from src.db.base import get_async_session
from src.repository.medical_history_repository import MedicalHistoryRepository
from src.schemas.medical_history_base import MedicalHistoryCreate, MedicalHistoryRead

router = APIRouter(prefix="/medical_history", tags=["Medical History"])

@router.post("/", response_model=MedicalHistoryRead)
async def create_history(
    history_in: MedicalHistoryCreate,
    session: AsyncSession = Depends(get_async_session)
):
    repo = MedicalHistoryRepository(session)
    return await repo.create(history_in)

@router.get("/", response_model=list[MedicalHistoryRead])
async def get_all_histories(
    full_name: Optional[str] = Query(default=None),
    admission_date: Optional[str] = Query(default=None),
    session: AsyncSession = Depends(get_async_session)
):
    repo = MedicalHistoryRepository(session)
    return await repo.get_filltered(full_name=full_name, admission_date=admission_date)

@router.get("/{history_id}", response_model=MedicalHistoryRead)
async def get_history_by_id(
    history_id: int,
    session: AsyncSession = Depends(get_async_session)
):
    repo = MedicalHistoryRepository(session)
    item = await repo.get_by_id(history_id)
    if not item:
        raise HTTPException(status_code=404, detail="Medical history not found")
    return MedicalHistoryRead.model_validate(item)

@router.put("/{history_id}", response_model=MedicalHistoryRead)
async def update_history(
    history_id: int,
    history_in: MedicalHistoryCreate,
    session: AsyncSession = Depends(get_async_session)
):
    repo = MedicalHistoryRepository(session)
    updated = await repo.update(history_id, history_in)
    if not updated:
        raise HTTPException(status_code=404, detail="Medical history not found")
    return MedicalHistoryRead.model_validate(updated)

@router.post("/{history_id}/cancel", response_model=MedicalHistoryRead)
async def cancel_history(
    history_id: int,
    session: AsyncSession = Depends(get_async_session)
):
    repo = MedicalHistoryRepository(session)
    cancelled = await repo.cancel(history_id)
    if not cancelled:
        raise HTTPException(status_code=404, detail="Medical history not found")
    return MedicalHistoryRead.model_validate(cancelled)

@router.post("/{history_id}/reactivate", response_model=MedicalHistoryRead)
async def reactivate_history(
    history_id: int,
    session: AsyncSession = Depends(get_async_session)
):
    repo = MedicalHistoryRepository(session)
    reactivated = await repo.reactivate(history_id)
    if not reactivated:
        raise HTTPException(status_code=404, detail="Medical history not found")
    return MedicalHistoryRead.model_validate(reactivated)
