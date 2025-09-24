import os

from celery import Celery
from dotenv import load_dotenv

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
