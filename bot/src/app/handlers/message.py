"""Attach all message handlers."""
from aiogram import types
from aiogram.dispatcher import FSMContext, filters

import app.handlers.constants_handlers as constants
from app.handlers.buttons_constants import ConstantButtonsData as cbd
from app.handlers.constant_buttons import contact_phone, welcome_menu
from app.handlers.forms.base_form import FormStatesGroup
from app.handlers.forms.keyboards import add_buttons, get_charity_keyboard, get_menu_keyboard
from app.orbi_bot import dp
from core.config import settings
from core.logger import logging
from utils.markup_processing import send_or_edit_message
from utils.menu_processing import parser_slug_text_with_buttons


@dp.message_handler(commands="start")
async def send_welcome(message: types.Message):
    """Reply to `/start` command."""
    try:
        text, buttons = await parser_slug_text_with_buttons(text_slug="welcome")
        buttons = get_menu_keyboard(buttons)
        add_buttons([contact_phone], buttons)
        await send_or_edit_message(text=text, buttons=buttons, message=message)
    except Exception:
        buttons = add_buttons([contact_phone])
        await message.answer(
            constants.BOT_NOT_AVAILABLE_ERROR_MESSAGE + f"<a>{settings.spare_url}</a>",
            parse_mode="HTML",
            reply_markup=buttons,
        )


@dp.message_handler(commands="help")
async def send_help(message: types.Message):
    """Reply to `/help` command."""
    buttons = add_buttons([welcome_menu, contact_phone])
    await message.answer(constants.BOT_HELP_MESSAGE, parse_mode="HTML", reply_markup=buttons)


@dp.message_handler(commands="about")
async def send_about(message: types.Message):
    """Reply to `/about` command."""
    buttons = add_buttons([welcome_menu, contact_phone])
    await message.answer(constants.BOT_ABOUT_MESSAGE, parse_mode="HTML", reply_markup=buttons)


@dp.callback_query_handler(text="/phone")
async def get_phone_number(call: types.CallbackQuery):
    """Send message with phone contact by command '/phone'."""
    text = cbd.get_phone_text()
    buttons = add_buttons([welcome_menu])
    await send_or_edit_message(text=text, buttons=buttons, callback_query=call)


@dp.callback_query_handler(text="form_menu", state=FormStatesGroup.fill_form)
async def form_menu(query: types.CallbackQuery, state: FSMContext):
    """Reply to start callback."""
    await form(query.message)
    await state.reset_data()


@dp.message_handler(filters.Text(contains="хочу помочь", ignore_case=True))
async def form(message: types.Message):
    """Form menu."""
    logging.info(f"{message.from_user.username}: {message.text}")
    buttons = get_charity_keyboard()
    add_buttons([welcome_menu, contact_phone], buttons)
    await message.answer(constants.WANT_TO_HELP_MESSAGE, reply_markup=buttons)
    await FormStatesGroup.set_form.set()
