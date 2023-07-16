import logging

from aiogram import types

import app.handlers.constants_handlers as constants
from app.handlers.constant_buttons import contact_phone, welcome_menu
from app.handlers.forms.keyboards import add_buttons, get_menu_keyboard
from app.middleware.antispam import rate_limit
from app.orbi_bot import dp
from core.config import settings
from core.exceptions import ApiClientException
from utils.markup_processing import send_or_edit_message
from utils.request_processing import get_request_data, post_request, up_counter
from utils.user_processing import check_user, post_user, update_user


@dp.message_handler(content_types=["text"])
@rate_limit(settings.sleep_time_in_seconds)
async def get_request(message: types.Message):
    """Reply to users requests."""
    try:
        id, text, buttons = await get_request_data(message.text.lower())
        if not await check_user(message.chat.id):
            await post_user(message.chat.id)
        if not text:
            if id:
                await up_counter(id)
            else:
                id = await post_request(message.text.lower())
                await update_user(message.chat.id, id)
            buttons = add_buttons([welcome_menu, contact_phone], buttons)
            await message.answer(constants.UNKNOWN_REPLY_MESSAGE, reply_markup=buttons)
        else:
            await up_counter(id)
            buttons = get_menu_keyboard(buttons)
            buttons = add_buttons([welcome_menu, contact_phone], buttons)
            await send_or_edit_message(text=text, buttons=buttons, message=message)
    except (TypeError, ApiClientException) as error:
        logging.error(f"Error in get_request() function: {str(error)}")
        buttons = add_buttons([contact_phone])
        await message.answer(
            constants.BOT_NOT_AVAILABLE_ERROR_MESSAGE + f"<a>{settings.spare_url}</a>",
            parse_mode="HTML",
            reply_markup=buttons,
        )
