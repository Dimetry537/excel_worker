from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
import jwt
from sqlalchemy import select
from sqlalchemy.orm import joinedload

from src.db.base import get_async_session
from src.repository.user_repository import UserRepository
from src.auth.utils import decode_jwt
from src.models.user import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_async_session)
) -> User:
    try:
        payload = decode_jwt(token)
        if payload.get("type") != "access":
            raise ValueError("Invalid token type")
        user_id = int(payload["sub"])
    except (jwt.PyJWTError, ValueError):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

    stmt = select(User).where(User.id == user_id).options(joinedload(User.roles))
    result = await db.execute(stmt)
    user = result.unique().scalars().one_or_none()
    if not user or not user.is_active:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Inactive user")
    return user

def role_required(required_roles: List[str]):
    async def check_role(current_user: User = Depends(get_current_user)):
        user_roles = [role.name for role in current_user.roles]
        if not any(role in user_roles for role in required_roles):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Insufficient permissions")
        return current_user
    return check_role
