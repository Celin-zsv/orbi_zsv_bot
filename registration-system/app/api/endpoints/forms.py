from fastapi import APIRouter

from app.api.enums import Form
from app.celery_worker import data_processing
from app.core.logger import log

EVENT_MESSAGE = "Get form data"

router = APIRouter()


def register_endpoint(form: Form):
    @router.post(f"/{form.value}")
    async def create_new_form(form_data: form.schema):
        data_processing.delay(form_data.dict(), form.name)
        log.info(form=form.name, form_data=form_data, event=EVENT_MESSAGE)
        return {"message": "Ваша анкета успешно сохранена!"}


register_endpoint(Form.ANOTHER_FORM)
register_endpoint(Form.BIRTHDAY_FORM)
register_endpoint(Form.RUN_FORM)
