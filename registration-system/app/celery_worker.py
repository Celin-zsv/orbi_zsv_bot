"""Создает Celery Worker."""
import asyncio

from celery import Celery, shared_task
from celery.utils.log import get_task_logger

from app.api.enums import Form
from app.core.config import settings
from app.core.db import AsyncSessionLocal

celery = Celery("tasks", broker=settings.celery_broker_url)
celery.conf.result_backend = settings.celery_result_backend
celery.conf.task_serializer = "pickle"
celery.conf.accept_content = ["application/json", "application/x-python-serialize"]
celery_log = get_task_logger(__name__)


async def save_form(form_data, form_type):
    form = Form[form_type]
    async with AsyncSessionLocal() as session:
        await form.crud.create(form_data, session)


@shared_task
def data_processing(form_data, form_type):
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
    loop.run_until_complete(save_form(form_data, form_type))
    celery_log.info(f"Эндпоинт сработал! data: {form_data}")
