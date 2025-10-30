import os
from dotenv import load_dotenv
from celery import Celery, shared_task
from celery.utils.log import get_task_logger
import asyncio
from datetime import date
from typing import Optional

from src.services.report_generator import generate_medical_history_report
from src.db.base import async_session, AsyncSession
from src.services.excel_service import export_medical_histories_to_excel

load_dotenv(".env")

celery = Celery(__name__)
celery.conf.update(
    broker_url=os.environ.get("CELERY_BROKER_URL"),
    result_backend=os.environ.get("CELERY_RESULT_BACKEND"),
    task_acks_late=True,
    task_default_retry_delay=30,
    task_max_retries=3,
    worker_pool='prefork', 
    worker_concurrency=4
)

logger = get_task_logger(__name__)

@shared_task
def say_hello():
    logger.info("Celery & Redis работают нормально!")

@shared_task(bind=True)
def export_medical_histories_task(
    self, file_path: str = "exports",
    full_name: Optional[str] = None,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None
) -> str:
    async def run():
        async with async_session() as session:
            return await export_medical_histories_to_excel(session, file_path, full_name, start_date, end_date)

    try:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        result = loop.run_until_complete(run())
        loop.close()
        logger.info(f"Экспорт завершён: {result}")
        return result
    except Exception as e:
        logger.error(f"Ошибка в экспорте: {e}")
        raise self.retry(exc=e)

@shared_task(bind=True, autoretry_for=(Exception,))
def generate_report_task(self, history_id: int) -> bytes:
    async def run():
        async with async_session() as session:
            buffer = await generate_medical_history_report(session, history_id)
            return buffer.getvalue()

    try:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        result = loop.run_until_complete(run())
        loop.close()
        logger.info(f"Отчёт для history_id {history_id} сгенерирован")
        return result
    except Exception as e:
        logger.error(f"Ошибка в генерации отчёта: {e}")
        raise self.retry(exc=e)