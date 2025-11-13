from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from src.db.base import get_async_session
from src.schemas.auth import RoleCreate, RoleRead
from src.repository.role_repository import RoleRepository
from src.auth.dependencies import role_required

router = APIRouter(prefix="/roles", tags=["roles"])

@router.post("/", response_model=RoleRead)
async def create_role(
    role: RoleCreate,
    db: AsyncSession = Depends(get_async_session),
    current_user = Depends(role_required(["admin"]))
):
    repo = RoleRepository(db)
    existing = await repo.get_by_name(role.name)
    if existing:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Role already exists")
    return await repo.create(role)

@router.get("/", response_model=List[RoleRead])
async def get_roles(
    db: AsyncSession = Depends(get_async_session),
    current_user = Depends(role_required(["admin"]))
):
    repo = RoleRepository(db)
    return await repo.get_all()
