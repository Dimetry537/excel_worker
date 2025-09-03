from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from src.db.config import ORACLE_HOST, ORACLE_PORT, ORACLE_USER, ORACLE_PASSWORD, ORACLE_SERVICE

ORACLE_DATABASE_URL = f"oracle+oracledb://{ORACLE_USER}:{ORACLE_PASSWORD}@{ORACLE_HOST}:{ORACLE_PORT}/?service_name={ORACLE_SERVICE}"

oracle_engine = create_async_engine(
    ORACLE_DATABASE_URL,
    echo=True
)

OracleSessionLocal = async_sessionmaker(
    bind=oracle_engine,
    autoflush=False,
    expire_on_commit=False,
    class_=AsyncSession
)

async def get_oracle_session() -> AsyncSession:
    async with OracleSessionLocal() as session:
        yield session
