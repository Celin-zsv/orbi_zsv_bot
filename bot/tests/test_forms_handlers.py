from unittest.mock import AsyncMock
from urllib.parse import urljoin

from aiogram.dispatcher import FSMContext

from app.handlers.constant_buttons import contact_phone, welcome_menu
from app.handlers.forms import another_help_form, base_form, birthday_form, constants, processing, run_form
from app.handlers.forms.keyboards import add_buttons, add_data_keyboard, cancel_keyboard, submit_keyboard
from core.config import settings
from core.exceptions import ApiClientException


async def test_set_another(monkeypatch, state: FSMContext):
    check_data = dict(
        form_data={},
        form=another_help_form.AnotherForm,
        next_field=constants.ADD_HELP_TEXT,
        url=urljoin(settings.registration_api_url, "form/another"),
    )
    mock_form_states = AsyncMock()
    monkeypatch.setattr(processing, "FormStatesGroup", mock_form_states)
    query = AsyncMock(data=constants.FILL_ANOTHER_FORM_CALLBACK)
    await processing.set_form_handlers(query, state)
    async with state.proxy() as data:
        state_data = dict(data)

    assert state_data == check_data
    mock_form_states.next.assert_called()
    query.message.answer.assert_called_with(
        processing.FORM_INFO[query.data]["start_text"], reply_markup=add_data_keyboard
    )


async def test_set_birthday(monkeypatch, state: FSMContext):
    check_data = dict(
        form_data={},
        form=birthday_form.BirthdayForm,
        next_field=constants.ADD_DATE_TEXT,
        url=urljoin(settings.registration_api_url, "form/birthday"),
    )
    mock_form_states = AsyncMock()
    monkeypatch.setattr(processing, "FormStatesGroup", mock_form_states)
    query = AsyncMock(data=constants.FILL_BIRTHDAY_FORM_CALLBACK)
    await processing.set_form_handlers(query, state)
    async with state.proxy() as data:
        state_data = dict(data)

    assert state_data == check_data
    mock_form_states.next.assert_called()
    query.message.answer.assert_called_with(
        processing.FORM_INFO[query.data]["start_text"], reply_markup=add_data_keyboard
    )


async def test_set_run(monkeypatch, state: FSMContext):
    check_data = dict(
        form_data={}, form=run_form.RunForm, next_field=None, url=urljoin(settings.registration_api_url, "form/run")
    )
    mock_form_states = AsyncMock()
    monkeypatch.setattr(processing, "FormStatesGroup", mock_form_states)
    query = AsyncMock(data=constants.FILL_RUN_FORM_CALLBACK)
    await processing.set_form_handlers(query, state)
    async with state.proxy() as data:
        state_data = dict(data)

    assert state_data == check_data
    mock_form_states.next.assert_called()
    query.message.answer.assert_called_with(
        processing.FORM_INFO[query.data]["start_text"], reply_markup=add_data_keyboard
    )


async def test_process_name(monkeypatch, state: FSMContext):
    mock_base_form = AsyncMock()
    monkeypatch.setattr(base_form, "BaseForm", mock_base_form)
    message = AsyncMock()
    async with state.proxy() as data:
        data["form_data"] = {}
    await base_form.process_name(message, state)
    async with state.proxy() as data:
        form_data = data["form_data"]

    assert form_data.get("name")
    mock_base_form.next.assert_called()
    message.answer.assert_called_with(constants.ADD_EMAIL_TEXT, reply_markup=cancel_keyboard)


async def test_process_email(state: FSMContext):
    message = AsyncMock()
    form = AsyncMock()
    async with state.proxy() as data:
        data["form_data"] = {"name": "Test_name"}
        data["form"] = form
        data["next_field"] = None
    await base_form.process_email(message, state)
    async with state.proxy() as data:
        form_data = data["form_data"]

    assert form_data.get("email")
    message.answer.assert_called_with(constants.SHOW_FORM_FIELDS_TEXT.format(**form_data), reply_markup=submit_keyboard)


async def test_process_email_next_field(state: FSMContext):
    message = AsyncMock()
    form = AsyncMock()
    async with state.proxy() as data:
        data["form_data"] = {"name": "Test_name"}
        data["form"] = form
        data["next_field"] = "next"
    await base_form.process_email(message, state)
    async with state.proxy() as data:
        form_data = data["form_data"]

    assert form_data.get("email")
    message.answer.assert_called_with("next", reply_markup=cancel_keyboard)


async def test_cancel(monkeypatch):
    mock_form_states = AsyncMock()
    monkeypatch.setattr(base_form, "FormStatesGroup", mock_form_states)
    query = AsyncMock()
    await base_form.cancel_handler(query)
    query.message.answer.assert_called_with(constants.FROM_CREATION_CANCELED_TEXT, reply_markup=add_data_keyboard)
    mock_form_states.fill_form.set.assert_called()


async def test_send_form(monkeypatch, state: FSMContext):
    monkeypatch.setattr(base_form.HttpClient, "__aenter__", AsyncMock())
    monkeypatch.setattr(base_form.HttpClient, "__aexit__", AsyncMock())
    query = AsyncMock()
    await state.set_state("test_state")
    async with state.proxy() as data:
        data["form_data"] = {}
        data["url"] = "test_url"
    await base_form.send_form(query, state)

    assert await state.get_state() is None
    query.message.edit_text.assert_called_with(
        constants.FORM_ACCEPTED_TEXT, reply_markup=add_buttons([welcome_menu, contact_phone])
    )


async def test_send_form_error(monkeypatch, state: FSMContext):
    async def mock_post_error(*args, **kwargs):
        raise ApiClientException

    mock_http_client = AsyncMock()
    mock_http_client.__aenter__ = AsyncMock(return_value=mock_http_client)
    mock_http_client.__aexit__ = AsyncMock(return_value=None)
    mock_http_client.post = mock_post_error
    monkeypatch.setattr(base_form, "HttpClient", lambda: mock_http_client)

    query = AsyncMock()
    async with state.proxy() as data:
        data["form_data"] = {}
        data["url"] = "test_url"

    await base_form.send_form(query, state)

    assert await state.get_state() is None
    query.message.edit_text.assert_any_call("Сервер недоступен, попробуйте позже")


async def test_process_help(state: FSMContext):
    message = AsyncMock()
    async with state.proxy() as data:
        data["form_data"] = {"name": "Test_name", "email": "test_email"}
    await another_help_form.process_help(message, state)
    async with state.proxy() as data:
        form_data = data["form_data"]

    assert form_data.get("help")
    message.answer.assert_called_with(
        constants.SHOW_ANOTHER_HELP_FORM_TEXT.format(**form_data), reply_markup=submit_keyboard
    )


async def test_process_date(state: FSMContext):
    message = AsyncMock(text="01.01.2091")
    async with state.proxy() as data:
        data["form_data"] = {"name": "Test_name", "email": "test_email"}
    await birthday_form.process_date(message, state)
    async with state.proxy() as data:
        form_data = data["form_data"]

    assert form_data.get("date")
    form_data["date"] = "01.01.2091"
    message.answer.assert_called_with(
        constants.SHOW_BIRTHDAY_FORM_FIELDS_TEXT.format(**form_data), reply_markup=submit_keyboard
    )
