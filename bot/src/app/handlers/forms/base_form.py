import logging

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

import app.handlers.forms.constants as constants
from app.handlers.constant_buttons import contact_phone, welcome_menu
from app.handlers.forms.keyboards import add_buttons, add_data_keyboard, cancel_keyboard, submit_keyboard
from app.orbi_bot import dp
from core.aio_client import HttpClient
from core.exceptions import ApiClientException


class FormStatesGroup(StatesGroup):
    set_form = State()
    fill_form = State()


class BaseForm(StatesGroup):
    name = State()
    email = State()


@dp.callback_query_handler(text=constants.ADD_FORM_DATA_CALLBACK, state="*")
async def add_name(query: types.CallbackQuery):
    """Form creation"""
    await query.message.answer(constants.ADD_NAME_TEXT, reply_markup=cancel_keyboard)
    await BaseForm.name.set()


@dp.message_handler(lambda message: message.text.isdigit(), state=BaseForm.name)
async def process_name_invalid(message: types.Message):
    """If name is invalid"""
    return await message.answer(constants.NAME_VALIDATION_ERROR_TEXT, reply_markup=cancel_keyboard)


@dp.message_handler(state=BaseForm.name)
async def process_name(message: types.Message, state: FSMContext):
    """Process username"""
    async with state.proxy() as data:
        data["form_data"]["name"] = message.text
    await message.answer(constants.ADD_EMAIL_TEXT, reply_markup=cancel_keyboard)
    await BaseForm.next()


@dp.message_handler(
    regexp=constants.EMAIL_REGEXP,
    state=BaseForm.email,
)
async def process_email(message: types.Message, state: FSMContext):
    """Process user email"""
    async with state.proxy() as data:
        data["form_data"]["email"] = message.text
        form_data = data["form_data"]
        form = data["form"]
        next_field = data["next_field"]
    if next_field is None:
        await message.answer(constants.SHOW_FORM_FIELDS_TEXT.format(**form_data), reply_markup=submit_keyboard)
    else:
        await message.answer(next_field, reply_markup=cancel_keyboard)
        await form.next()


@dp.message_handler(state=BaseForm.email)
async def process_invalid_email(message: types.Message):
    """If email is invalid"""
    return await message.answer(constants.EMAIL_VALIDATION_ERROR_TEXT, reply_markup=cancel_keyboard)


@dp.callback_query_handler(text=constants.CANCEL_BUTTON_CALLBACK, state="*")
async def cancel_handler(query: types.CallbackQuery):
    """Allow user to cancel any action"""
    await query.message.answer(constants.FROM_CREATION_CANCELED_TEXT, reply_markup=add_data_keyboard)
    await FormStatesGroup.fill_form.set()


@dp.callback_query_handler(text=constants.SEND_FORM_BUTTON_CALLBACK, state="*")
async def send_form(query: types.CallbackQuery, state: FSMContext):
    """Sending completed form"""
    async with state.proxy() as data:
        form_data = data["form_data"]
        url = data["url"]
    try:
        async with HttpClient() as client:
            await client.post(url, form_data)
    except ApiClientException as error:
        logging.error(f"Error while sending form with send_form() function: {str(error)}")
        await query.message.edit_text(
            "Сервер недоступен, попробуйте позже",
        )
    else:
        await query.message.edit_text(
            constants.FORM_ACCEPTED_TEXT, reply_markup=add_buttons([welcome_menu, contact_phone])
        )
    finally:
        await state.finish()
