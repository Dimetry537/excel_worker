import os
import asyncio

from celery import Celery, shared_task
from dotenv import load_dotenv

from src.db.base import async_session
from src.services.excel_service import export_medical_histories_to_excel

load_dotenv(".env")

celery = Celery(__name__)

celery.conf.update(
    broker_url = os.environ.get("CELERY_BROKER_URL"),
    result_backend = os.environ.get("CELERY_RESULT_BACKEND")
)


@celery.task
def say_hello():
    print("Celery & Redis работают нормально!")

say_hello.delay()

@shared_task
def export_medical_histories_task(file_path: str = "exports") -> str:
    async def run_export():
        async with async_session() as session:
            return await export_medical_histories_to_excel(session, file_path)

    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

    try:
        future = asyncio.ensure_future(run_export(), loop=loop)
        result = loop.run_until_complete(future)
        return result
    except Exception as e:
        print(f"Error in export task: {e}")
        raise
    finally:

        if loop.is_closed():
            loop.close()
