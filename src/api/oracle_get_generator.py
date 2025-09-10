from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from src.db.oracle_db import get_db_session

router = APIRouter(prefix="/oracle", tags=["Oracle DB"])

@router.get("/oracle-test")
async def oracle_test(session: AsyncSession = Depends(get_db_session)):
    result = await session.execute(text("SELECT sysdate FROM dual"))
    row = await result.fetchone()
    return {"sysdate": str(row[0])}
