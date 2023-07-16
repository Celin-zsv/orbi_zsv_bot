from datetime import datetime

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

import app.handlers.forms.constants as constants
from app.handlers.forms.keyboards import cancel_keyboard, submit_keyboard
from app.orbi_bot import dp


class BirthdayForm(StatesGroup):
    date = State()


@dp.message_handler(future_date=False, state=BirthdayForm.date)
async def process_invalid_date(message: types.Message):
    """
    If date is invalid
    """
    return await message.answer(constants.DATE_VALIDATION_ERROR_TEXT, reply_markup=cancel_keyboard)


@dp.message_handler(state=BirthdayForm.date)
async def process_date(message: types.Message, state: FSMContext):
    """
    Process user date
    """
    async with state.proxy() as data:
        data["form_data"]["date"] = message.text
        form_data = data["form_data"].copy()
        data["form_data"]["date"] = datetime.strptime(message.text, "%d.%m.%Y").date().isoformat()
    await message.answer(constants.SHOW_BIRTHDAY_FORM_FIELDS_TEXT.format(**form_data), reply_markup=submit_keyboard)
