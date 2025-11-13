from typing import Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException
from sqlalchemy.orm import joinedload

from src.models.user import User
from src.models.role import Role
from src.schemas.auth import UserCreate, UserRead, UserUpdate
from src.auth.utils import hash_password, verify_password
from src.repository.base_repository import BaseRepository

class UserRepository(BaseRepository[User]):
    def __init__(self, session: AsyncSession):
        super().__init__(session, User)

    async def create(self, obj_in: UserCreate) -> UserRead:
        user_data = {
            "username": obj_in.username,
            "hashed_password": hash_password(obj_in.password),
            "is_active": True
        }
        user = await super().create(user_data)
        
        await self._assign_roles(user, obj_in.role_names)
        stmt = select(User).where(User.id == user.id).options(joinedload(User.roles))
        result = await self.session.execute(stmt)
        user = result.unique().scalars().one()
        return UserRead.model_validate(user)

    async def update(self, obj_id: int, obj_in: UserUpdate) -> Optional[UserRead]:
        update_data = obj_in.dict(exclude_unset=True)
        if "password" in update_data:
            update_data["hashed_password"] = hash_password(update_data.pop("password"))
        
        updated_user = await super().update(obj_id, update_data)
        if not updated_user:
            return None
        
        if obj_in.role_names is not None:
            stmt = select(User).where(User.id == obj_id).options(joinedload(User.roles))
            result = await self.session.execute(stmt)
            updated_user = result.unique().scalars().one()
            
            updated_user.roles = []
            await self.session.commit()
            await self._assign_roles(updated_user, obj_in.role_names)
        
        stmt = select(User).where(User.id == obj_id).options(joinedload(User.roles))
        result = await self.session.execute(stmt)
        updated_user = result.unique().scalars().one()
        return UserRead.model_validate(updated_user)

    async def get_by_username(self, username: str) -> Optional[User]:
        stmt = select(User).where(User.username == username).options(joinedload(User.roles))
        result = await self.session.execute(stmt)
        return result.unique().scalars().one_or_none()

    async def get_by_id(self, id: int) -> Optional[User]:
        stmt = select(User).where(User.id == id).options(joinedload(User.roles))
        result = await self.session.execute(stmt)
        return result.unique().scalars().one_or_none()

    async def get_all(self) -> List[UserRead]:
        stmt = select(User).options(joinedload(User.roles))
        result = await self.session.execute(stmt)
        users = result.unique().scalars().all()
        return [UserRead.model_validate(user) for user in users]

    async def authenticate(self, username: str, password: str) -> Optional[User]:
        user = await self.get_by_username(username)
        if user and verify_password(password, user.hashed_password):
            return user
        return None

    async def _assign_roles(self, user: User, role_names: List[str]):
        stmt = select(User).where(User.id == user.id).options(joinedload(User.roles))
        result = await self.session.execute(stmt)
        user = result.unique().scalars().one()
        
        for role_name in role_names:
            role = await self._get_role_by_name(role_name)
            if role:
                if role not in user.roles:
                    user.roles.append(role)
            else:
                raise HTTPException(status_code=400, detail=f"Role '{role_name}' not found")
        await self.session.commit()
        await self.session.refresh(user)

    async def _get_role_by_name(self, name: str) -> Optional[Role]:
        stmt = select(Role).where(Role.name == name)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()
