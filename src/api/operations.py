from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from src.db.base import get_async_session
from src.repository.operation_repository import OperationRepository
from src.schemas.operation_base import OperationCreate, OperationRead
from src.auth.dependencies import get_current_user

router = APIRouter(
    prefix="/operations",
    tags=["Operations"],
    dependencies=[Depends(get_current_user)]
)


@router.post("/", response_model=OperationRead)
async def create_operation(
    operation_in: OperationCreate,
    session: AsyncSession = Depends(get_async_session)
):
    repo = OperationRepository(session)
    return await repo.create(operation_in)


@router.get("/", response_model=List[OperationRead])
async def get_operations(session: AsyncSession = Depends(get_async_session)):
    repo = OperationRepository(session)
    return await repo.get_all()


@router.get("/{operation_id}", response_model=OperationRead)
async def get_operation_by_id(
    operation_id: int,
    session: AsyncSession = Depends(get_async_session)
):
    repo = OperationRepository(session)
    operation = await repo.get_by_id(operation_id)
    if not operation:
        raise HTTPException(status_code=404, detail="Операция не найдена")
    return operation


@router.put("/{operation_id}", response_model=OperationRead)
async def update_operation(
    operation_id: int,
    operation_in: OperationCreate,
    session: AsyncSession = Depends(get_async_session)
):
    repo = OperationRepository(session)
    updated = await repo.update(operation_id, operation_in)
    if not updated:
        raise HTTPException(status_code=404, detail="Операция не найдена")
    return updated


@router.delete("/{operation_id}", response_model=OperationRead)
async def delete_operation(
    operation_id: int,
    session: AsyncSession = Depends(get_async_session)
):
    repo = OperationRepository(session)
    deleted = await repo.delete(operation_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Операция не найдена")
    return deleted


@router.get("/history/{history_id}", response_model=List[OperationRead])
async def get_operations_by_history_id(
    history_id: int,
    session: AsyncSession = Depends(get_async_session)
):
    repo = OperationRepository(session)
    operations = await repo.get_by_history_id(history_id)
    if not operations:
        raise HTTPException(status_code=404, detail="Операции для этой истории не найдены")
    return operations
