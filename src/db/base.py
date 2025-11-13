from typing import AsyncGenerator
from datetime import datetime, timezone
from sqlalchemy  import Column
from sqlalchemy.dialects.postgresql import TIMESTAMP
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine

Base = declarative_base()

class TimestampMixin:
    created_at = Column(TIMESTAMP(timezone=True), default=datetime.now(timezone.utc))
    updated_at = Column(TIMESTAMP(timezone=True), default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))


from src.db.config import settings

DATABASE_URL = f"postgresql+asyncpg://{settings.db_user}:{settings.db_pass}@{settings.db_host}:{settings.db_port}/{settings.db_name}"

engine = create_async_engine(DATABASE_URL, echo=True)

async_session = sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False
)

async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        yield session

from src.models.user_role import user_roles
