from aiogram.types import InlineKeyboardButton

from app.handlers.buttons_constants import ConstantButtonsData as cbd

welcome_menu = InlineKeyboardButton(cbd.menu_text.value, callback_data=cbd.menu_callback_text.value)
contact_phone = InlineKeyboardButton(cbd.phone_text.value, callback_data=cbd.phone_callback_command.value)
