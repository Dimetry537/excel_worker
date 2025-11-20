from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.base import get_async_session
from src.repository.user_repository import UserRepository
from src.schemas.auth import Token
from src.auth.utils import create_access_token, create_refresh_token
from src.schemas.auth import Token, UserRead
from src.auth.dependencies import get_current_user
from src.models.user import User
from src.auth.utils import decode_jwt

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/login", response_model=Token)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_async_session)
):
    repo = UserRepository(db)
    user = await repo.authenticate(form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    return Token(access_token=create_access_token(user), refresh_token=create_refresh_token(user))

@router.get("/me", response_model=UserRead)
async def read_users_me(current_user: User = Depends(get_current_user)):
    return UserRead.model_validate(current_user)


@router.post("/refresh", response_model=Token)
async def refresh_token(
    refresh_token: str,
    db: AsyncSession = Depends(get_async_session),
):
    try:
        payload = decode_jwt(refresh_token)
        if payload.get("type") != "refresh":
            raise HTTPException(status_code=401, detail="Invalid refresh token")

        user_id = int(payload["sub"])
        repo = UserRepository(db)
        user = await repo.get_by_id(user_id)
        if not user:
            raise HTTPException(status_code=401, detail="User not found")

        return Token(
            access_token=create_access_token(user),
            refresh_token=create_refresh_token(user),
        )
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid or expired refresh token")


@router.post("/logout")
async def logout():
    return {"detail": "Successfully logged out"}