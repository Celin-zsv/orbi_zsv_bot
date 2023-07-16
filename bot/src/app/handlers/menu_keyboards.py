import logging

from aiogram import types
from aiogram.dispatcher.filters import Text

import app.handlers.constants_handlers as constant
from app.handlers.constant_buttons import contact_phone, welcome_menu
from app.handlers.forms.keyboards import add_buttons, get_menu_keyboard
from app.orbi_bot import dp
from core.config import settings
from core.exceptions import ApiClientException
from utils.markup_processing import send_or_edit_message
from utils.menu_processing import parser_slug_text_with_buttons


@dp.callback_query_handler(Text(startswith="slug_"))
async def handle_menu_callback(callback_query: types.CallbackQuery):
    callback_data = callback_query.data.split("_")[1]
    try:
        menu_text, menu_buttons = await parser_slug_text_with_buttons(callback_data)
        additional_buttons = [welcome_menu, contact_phone] if callback_data != "welcome" else [contact_phone]
        menu_buttons = add_buttons(additional_buttons, get_menu_keyboard(menu_buttons))
    except ApiClientException as error:
        logging.error(f"Error in handle_menu_callback() function with callback data '{callback_data}': {str(error)}")
        menu_text = constant.BOT_NOT_AVAILABLE_ERROR_MESSAGE + f"<a>{settings.spare_url}</a>"
        menu_buttons = add_buttons([contact_phone])
    await send_or_edit_message(text=menu_text, buttons=menu_buttons, callback_query=callback_query)
