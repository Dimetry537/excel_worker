import os
from dotenv import load_dotenv
from celery import Celery, shared_task
from celery.utils.log import get_task_logger
import asyncio
from datetime import datetime
from typing import Optional

from src.services.report_generator import generate_medical_history_report
from src.db.base import async_session
from src.services.excel_service import export_medical_histories_to_excel

load_dotenv(".env")

celery = Celery(__name__)
celery.conf.update(
    broker_url=os.environ.get("CELERY_BROKER_URL"),
    result_backend=os.environ.get("CELERY_RESULT_BACKEND"),
    task_acks_late=True,
    task_default_retry_delay=30,
    task_max_retries=3,
    worker_concurrency=10
)

logger = get_task_logger(__name__)

@shared_task(bind=True)
def generate_report_task(self, history_id: int) -> bytes:
    try:
        loop = asyncio.get_event_loop()
        is_new_loop = False
    except RuntimeError:
        loop = asyncio.new_event_loop()
        is_new_loop = True
    asyncio.set_event_loop(loop)

    async def run():
        async with async_session() as session:
            buffer = await generate_medical_history_report(session, history_id)
            return buffer.getvalue()

    try:
        coro = run()
        future = asyncio.ensure_future(coro, loop=loop)
        result = loop.run_until_complete(future)
        logger.info(f"Отчёт для history_id {history_id} сгенерирован")
        return result
    except Exception as e:
        logger.error(f"Ошибка в генерации отчёта: {e}")
        raise self.retry(exc=e)
    finally:
        if is_new_loop and not loop.is_closed():
            loop.close()

@shared_task(bind=True)
def export_medical_histories_task(
    self,
    full_name: Optional[str] = None,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None
) -> str:
    try:
        loop = asyncio.get_event_loop()
        is_new_loop = False
    except RuntimeError:
        loop = asyncio.new_event_loop()
        is_new_loop = True
    asyncio.set_event_loop(loop)

    async def run():
        async with async_session() as session:
            parsed_start_date = None
            if start_date:
                try:
                    parsed_start_date = datetime.strptime(start_date, '%d.%m.%Y').date()
                except ValueError:
                    parsed_start_date = datetime.strptime(start_date, '%Y-%m-%d').date()

            parsed_end_date = None
            if end_date:
                try:
                    parsed_end_date = datetime.strptime(end_date, '%d.%m.%Y').date()
                except ValueError:
                    parsed_end_date = datetime.strptime(end_date, '%Y-%m-%d').date()

            return await export_medical_histories_to_excel(
                session,
                full_name=full_name,
                start_date=parsed_start_date,
                end_date=parsed_end_date
            )

    try:
        coro = run()
        future = asyncio.ensure_future(coro, loop=loop)
        result = loop.run_until_complete(future)
        logger.info(f"Экспорт завершён: {result}")
        return result
    except Exception as e:
        logger.error(f"Ошибка в экспорте: {e}")
        raise self.retry(exc=e)
    finally:
        if is_new_loop and not loop.is_closed():
            loop.close()
