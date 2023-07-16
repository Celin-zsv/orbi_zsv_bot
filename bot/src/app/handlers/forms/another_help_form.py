from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

import app.handlers.forms.constants as constants
from app.handlers.forms.keyboards import cancel_keyboard, submit_keyboard
from app.orbi_bot import dp


class AnotherForm(StatesGroup):
    help_text = State()


@dp.message_handler(lambda message: message.text.isdigit(), state=AnotherForm.help_text)
async def process_invalid_help(message: types.Message):
    """
    If help is invalid
    """
    return await message.answer(constants.HELP_TEXT_VALIDATION_ERROR, reply_markup=cancel_keyboard)


@dp.message_handler(state=AnotherForm.help_text)
async def process_help(message: types.Message, state: FSMContext):
    """
    Process user help
    """
    async with state.proxy() as data:
        data["form_data"]["help"] = message.text
        form_data = data["form_data"]
    await message.answer(constants.SHOW_ANOTHER_HELP_FORM_TEXT.format(**form_data), reply_markup=submit_keyboard)
