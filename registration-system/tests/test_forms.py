import time
from datetime import date, timedelta
from http import HTTPStatus

from sqlalchemy import select

from app.models.another_form import AnotherForm
from app.models.birthday_form import BirthdayForm
from app.models.run_form import RunForm


async def select_by_name(session, form, name):
    db_obj = await session.execute(select(form).where(form.name == name))
    return db_obj.scalars().all()


async def test_another_form(celery_session_worker, test_client, init_db_session):
    data = {"name": "Test", "email": "test@mail.com", "help": "test_help"}
    response = test_client.post("/form/another", json=data)
    time.sleep(1)
    db_obj = await select_by_name(init_db_session, AnotherForm, data["name"])

    assert response.status_code == HTTPStatus.OK, "Неверный статус-код another_form"
    assert db_obj, "Объект another_form не сохраняется в базу данных"


async def test_birthday_form(celery_session_worker, test_client, init_db_session):
    data = {"name": "Test", "email": "test@mail.com", "date": (date.today() + timedelta(days=365)).isoformat()}
    response = test_client.post("/form/birthday", json=data)
    time.sleep(1)
    db_obj = await select_by_name(init_db_session, BirthdayForm, data["name"])

    assert response.status_code == HTTPStatus.OK, "Неверный статус-код birthday_form"
    assert db_obj, "Объект birthday_form не сохраняется в базу данных"


async def test_run_form(celery_session_worker, test_client, init_db_session):
    data = {"name": "Test", "email": "test@mail.com"}
    response = test_client.post("/form/run", json=data)
    time.sleep(1)
    db_obj = await select_by_name(init_db_session, RunForm, data["name"])

    assert response.status_code == HTTPStatus.OK, "Неверный статус-код run_form"
    assert db_obj, "Объект run_form не сохраняется в базу данных"
