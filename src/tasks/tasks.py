# import os
# import asyncio

# from celery import Celery, shared_task
# from dotenv import load_dotenv

# from src.services.report_generator import generate_medical_history_report
# from src.db.base import async_session
# from src.services.excel_service import export_medical_histories_to_excel

# load_dotenv(".env")

# celery = Celery(__name__)

# celery.conf.update(
#     broker_url = os.environ.get("CELERY_BROKER_URL"),
#     result_backend = os.environ.get("CELERY_RESULT_BACKEND")
# )


# @celery.task
# def say_hello():
#     print("Celery & Redis работают нормально!")

# say_hello.delay()

# @shared_task
# def export_medical_histories_task(file_path: str = "exports") -> str:
#     async def run_export():
#         async with async_session() as session:
#             return await export_medical_histories_to_excel(session, file_path)

#     try:
#         loop = asyncio.get_event_loop()
#     except RuntimeError:
#         loop = asyncio.new_event_loop()
#         asyncio.set_event_loop(loop)

#     try:
#         future = asyncio.ensure_future(run_export(), loop=loop)
#         result = loop.run_until_complete(future)
#         return result
#     except Exception as e:
#         print(f"Error in export task: {e}")
#         raise
#     finally:

#         if loop.is_closed():
#             loop.close()


# @shared_task
# def generate_report_task(history_id: int):
#     import asyncio
#     async def run():
#         async with async_session() as session:
#             buffer = await generate_medical_history_report(session, history_id)
#             return buffer.getvalue()
#     return asyncio.run(run())

import os
from dotenv import load_dotenv
from celery import Celery, shared_task
from celery.utils.log import get_task_logger
import asyncio

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
    task_max_retries=3
)

logger = get_task_logger(__name__)

@shared_task
def say_hello():
    logger.info("Celery & Redis работают нормально!")


@shared_task(bind=True, autoretry_for=(Exception,))
def export_medical_histories_task(self, file_path: str = "exports") -> str:
    async def run():
        async with async_session() as session:
            return await export_medical_histories_to_excel(session, file_path)

    try:
        result = asyncio.run(run())
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
        result = asyncio.run(run())
        logger.info(f"Отчёт для history_id {history_id} сгенерирован")
        return result
    except Exception as e:
        logger.error(f"Ошибка в генерации отчёта: {e}")
        raise self.retry(exc=e)
    