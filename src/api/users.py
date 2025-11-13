from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from src.db.base import get_async_session
from src.schemas.auth import UserCreate, UserRead, UserUpdate
from src.repository.user_repository import UserRepository
from src.auth.dependencies import get_current_user, role_required
from src.models.user import User

router = APIRouter(prefix="/users", tags=["users"])

@router.post("/", response_model=UserRead)
async def create_user(
    user: UserCreate,
    db: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(role_required(["admin"]))
):
    repo = UserRepository(db)
    existing = await repo.get_by_username(user.username)
    if existing:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username already registered")
    return await repo.create(user)

@router.get("/", response_model=List[UserRead])
async def get_users(
    db: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(role_required(["admin"]))
):
    repo = UserRepository(db)
    return await repo.get_all()

@router.get("/{user_id}", response_model=UserRead)
async def get_user(
    user_id: int,
    db: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(get_current_user)
):
    repo = UserRepository(db)
    user = await repo.get_by_id(user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    if current_user.id != user_id and "admin" not in [role.name for role in current_user.roles]:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Insufficient permissions")
    return UserRead.model_validate(user)

@router.patch("/{user_id}", response_model=UserRead)
async def update_user(
    user_id: int,
    update_data: UserUpdate,
    db: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(get_current_user)
):
    if current_user.id != user_id and "admin" not in [role.name for role in current_user.roles]:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Insufficient permissions")
    
    repo = UserRepository(db)
    updated = await repo.update(user_id, update_data)
    if not updated:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return updated

@router.delete("/{user_id}", response_model=UserRead)
async def delete_user(
    user_id: int,
    db: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(role_required(["admin"]))
):
    repo = UserRepository(db)
    deleted = await repo.delete(user_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return UserRead.model_validate(deleted)
