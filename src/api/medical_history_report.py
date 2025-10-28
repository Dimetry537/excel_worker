from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from sqlalchemy.ext.asyncio import AsyncSession
from io import BytesIO

from src.db.base import get_async_session
from src.services.report_generator import generate_medical_history_report
from src.tasks.tasks import generate_report_task

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


@router.post("/{history_id}/report-async")
def start_generate_report_async(history_id: int):
    task = generate_report_task.delay(history_id)
    return {"task_id": task.id, "message": "Задача на генерацию отчёта запущена. Проверьте статус по /tasks/{task_id}"}


@router.get("/report-task/{task_id}")
async def get_report_from_task(task_id: str):
    from celery.result import AsyncResult
    task_result = AsyncResult(task_id)
    if task_result.status != "SUCCESS":
        raise HTTPException(status_code=400, detail=f"Задача не готова. Статус: {task_result.status}")

    buffer = BytesIO(task_result.result)
    headers = {
        "Content-Disposition": "attachment; filename=medical_history_report.docx",
        "Content-Type": "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    }
    return StreamingResponse(buffer, headers=headers)