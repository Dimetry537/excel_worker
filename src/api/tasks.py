from celery.result import AsyncResult
from src.tasks.tasks import celery
from fastapi import APIRouter, Depends
from src.auth.dependencies import get_current_user

router = APIRouter(
    prefix="/tasks",
    tags=["Tasks"],
    dependencies=[Depends(get_current_user)]
)

@router.get("/{task_id}")
def get_task_status(task_id: str):
    result = AsyncResult(task_id, app=celery)
    return {"task_id": task_id, "status": result.status, "result": result.result}
