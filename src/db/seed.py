import asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from src.db.base import get_async_session
from src.models.user_role import user_roles
from src.models.role import Role
from src.models.user import User
from src.auth.utils import hash_password
from src.db.config import settings

async def seed_data(session: AsyncSession):
    roles = ["surgeon", "nurse", "admin"]
    for role_name in roles:
        existing = await session.execute(select(Role).where(Role.name == role_name))
        if not existing.scalar_one_or_none():
            role = Role(name=role_name)
            session.add(role)
    
    await session.commit()

    admin_username = settings.admin_username
    admin_password = settings.admin_password
    existing_user = await session.execute(select(User).where(User.username == admin_username))
    if not existing_user.scalar_one_or_none():
        hashed = hash_password(admin_password)
        admin = User(username=admin_username, hashed_password=hashed, is_active=True)
        admin_role = await session.execute(select(Role).where(Role.name == "admin"))
        admin.roles.append(admin_role.scalar_one_or_none())
        session.add(admin)
        await session.commit()

async def main():
    async for session in get_async_session():
        await seed_data(session)
        break

if __name__ == "__main__":
    asyncio.run(main())
