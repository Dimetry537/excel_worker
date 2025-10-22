from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from sqlalchemy.ext.asyncio import AsyncSession
from src.db.base import get_async_session
from src.services.report_generator import generate_medical_history_report

router = APIRouter(prefix="/medical-histories", tags=["medical-histories"])

@router.get("/{history_id}/report")
async def get_medical_history_report(history_id: int, db: AsyncSession = Depends(get_async_session)):
    try:
        buffer = await generate_medical_history_report(db, history_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка генерации отчёта: {str(e)}")

    headers = {
        "Content-Disposition": f"attachment; filename=medical_history_{history_id}.docx",
        "Content-Type": "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    }
    return StreamingResponse(buffer, headers=headers)
