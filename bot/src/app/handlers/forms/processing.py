import logging
from urllib.parse import urljoin

from aiogram import types
from aiogram.dispatcher import FSMContext

import app.handlers.forms.constants as constants
from app.handlers.forms.another_help_form import AnotherForm
from app.handlers.forms.base_form import FormStatesGroup
from app.handlers.forms.birthday_form import BirthdayForm
from app.handlers.forms.keyboards import add_data_keyboard
from app.handlers.forms.run_form import RunForm
from app.orbi_bot import dp
from core.config import settings

FORM_INFO = {
    constants.FILL_BIRTHDAY_FORM_CALLBACK: {
        "form": BirthdayForm,
        "start_text": constants.BIRTHDAY_FORM_START_TEXT,
        "next_field": constants.ADD_DATE_TEXT,
        "url": urljoin(settings.registration_api_url, "form/birthday"),
    },
    constants.FILL_RUN_FORM_CALLBACK: {
        "form": RunForm,
        "start_text": constants.RUN_FORM_START_TEXT,
        "next_field": None,
        "url": urljoin(settings.registration_api_url, "form/run"),
    },
    constants.FILL_ANOTHER_FORM_CALLBACK: {
        "form": AnotherForm,
        "start_text": constants.ANOTHER_FORM_START_TEXT,
        "next_field": constants.ADD_HELP_TEXT,
        "url": urljoin(settings.registration_api_url, "form/another"),
    },
}


@dp.callback_query_handler(state=FormStatesGroup.set_form)
async def set_form_handlers(query: types.CallbackQuery, state: FSMContext):
    logging.info(f"{query.message.from_user.username}: {query.message.text}")
    async with state.proxy() as data:
        data["form_data"] = {}
        data["form"] = FORM_INFO[query.data]["form"]
        data["next_field"] = FORM_INFO[query.data]["next_field"]
        data["url"] = FORM_INFO[query.data]["url"]
    await query.message.answer(FORM_INFO[query.data]["start_text"], reply_markup=add_data_keyboard)
    await FormStatesGroup.next()
