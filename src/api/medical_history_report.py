from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from io import BytesIO

from src.tasks.tasks import generate_report_task
from src.auth.dependencies import get_current_user

router = APIRouter(
    prefix="/medical-histories",
    tags=["medical-histories"],
    dependencies=[Depends(get_current_user)]
)

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
