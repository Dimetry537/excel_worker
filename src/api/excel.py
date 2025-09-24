from fastapi import APIRouter, Depends
from fastapi.responses import FileResponse
from sqlalchemy.ext.asyncio import AsyncSession
from src.db.base import get_async_session
from src.services.excel_service import export_medical_histories_to_excel
import os

router = APIRouter(prefix="/excel", tags=["excel"])

@router.get("/export", response_class=FileResponse)
async def export_to_excel(db: AsyncSession = Depends(get_async_session)):
    file_path = await export_medical_histories_to_excel(db)

    response = FileResponse(
        path=file_path,
        filename=os.path.basename(file_path),
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

    return response
