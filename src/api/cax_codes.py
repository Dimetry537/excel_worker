from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from src.schemas.cax_code import CaxCodeCreate, CaxCodeRead
from src.repository.cax_code_repository import CaxCodeRepository
from src.db.base import get_async_session
from src.auth.dependencies import get_current_user

router = APIRouter(
    prefix="/cax_codes",
    tags=["Cax Codes"],
    dependencies=[Depends(get_current_user)]
)

@router.post("/", response_model=CaxCodeRead)
async def create_cax_code(
    cax_in: CaxCodeCreate,
    session: AsyncSession = Depends(get_async_session)
):
    repo = CaxCodeRepository(session)
    return await repo.create(cax_in)

@router.get("/", response_model=list[CaxCodeRead])
async def get_all_cax_codes(
    session: AsyncSession = Depends(get_async_session)
):
    repo = CaxCodeRepository(session)
    codes = await repo.get_all()
    return [CaxCodeRead.model_validate(c) for c in codes]

@router.get("/{cax_id}", response_model=CaxCodeRead)
async def get_cax_code_by_id(
    cax_id: int,
    session: AsyncSession = Depends(get_async_session)
):
    repo = CaxCodeRepository(session)
    code = await repo.get_by_id(cax_id)
    if not code:
        raise HTTPException(status_code=404, detail="Cax Code not found")
    return CaxCodeRead.model_validate(code)

@router.put("/{cax_id}", response_model=CaxCodeRead)
async def update_cax_code(
    cax_id: int,
    cax_in: CaxCodeCreate,
    session: AsyncSession = Depends(get_async_session)
):
    repo = CaxCodeRepository(session)
    updated =  await repo.update(cax_id, cax_in)
    if not updated:
        raise HTTPException(status_code=404, detail="Cax Code not found")
    return CaxCodeRead.model_validate(updated)

@router.delete("/{cax_id}", response_model=CaxCodeRead)
async def delete_cax_code(
    cax_id: int,
    session: AsyncSession = Depends(get_async_session)
):
    repo = CaxCodeRepository(session)
    deleted = await repo.delete(cax_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Cax Code not found")
    return CaxCodeRead.model_validate(deleted)

@router.patch("/{cax_id}/toggle_active", response_model=CaxCodeRead)
async def toggle_cax_code_active(
    cax_id: int,
    session: AsyncSession = Depends(get_async_session)
):
    repo = CaxCodeRepository(session)
    toggled = await repo.toggle_active(cax_id)
    if not toggled:
        raise HTTPException(status_code=404, detail="Cax Code not found")
    return toggled
