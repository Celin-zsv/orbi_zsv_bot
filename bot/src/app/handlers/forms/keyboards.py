from typing import Optional

from aiogram import types

import app.handlers.forms.constants as constants
from app.handlers.utils import sort_buttons


def get_back_form_keyboard():
    markup = types.InlineKeyboardMarkup()
    markup.add(
        types.InlineKeyboardButton(constants.BACK_BUTTON_TEXT, callback_data=constants.BACK_FORM_BUTTON_CALLBACK)
    )
    return markup


def add_buttons(
    buttons: list[types.InlineKeyboardButton], markup: Optional[types.InlineKeyboardMarkup] = None
) -> types.InlineKeyboardMarkup:
    """
    Create InlineMarkup and add new buttons
    or add buttons to exist markup like new row.
    """

    if not markup:
        markup = types.InlineKeyboardMarkup()
    for button in buttons:
        markup.add(button)
    return markup


def get_cancel_keyboard():
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton(constants.CANCEL_BUTTON_TEXT, callback_data=constants.CANCEL_BUTTON_CALLBACK))
    return markup


def get_charity_keyboard():
    markup = types.InlineKeyboardMarkup()
    markup.add(
        types.InlineKeyboardButton(
            constants.FILL_BIRTHDAY_FORM_BUTTON_TEXT, callback_data=constants.FILL_BIRTHDAY_FORM_CALLBACK
        )
    ).add(
        types.InlineKeyboardButton(constants.FILL_RUN_FORM_BUTTON_TEXT, callback_data=constants.FILL_RUN_FORM_CALLBACK)
    ).add(
        types.InlineKeyboardButton(constants.DONATION_BUTTON_TEXT, callback_data=constants.DONATION_BUTTON_CALLBACK)
    ).add(
        types.InlineKeyboardButton(
            constants.ANOTHER_FORM_BUTTON_TEXT, callback_data=constants.FILL_ANOTHER_FORM_CALLBACK
        )
    )
    return markup


def get_submit_keyboard():
    markup = types.InlineKeyboardMarkup()
    markup.add(
        types.InlineKeyboardButton(constants.SEND_FORM_BUTTON_TEXT, callback_data=constants.SEND_FORM_BUTTON_CALLBACK)
    )
    markup.add(types.InlineKeyboardButton(constants.CANCEL_BUTTON_TEXT, callback_data=constants.CANCEL_BUTTON_CALLBACK))
    return markup


def get_menu_keyboard(data):
    """Функция создания меню с кнопками."""
    markup = types.InlineKeyboardMarkup()
    buttons = sort_buttons(data)
    for button in buttons:
        if "slug" in button:
            markup.add(types.InlineKeyboardButton(button.get("cover_text"), callback_data=f'slug_{button.get("slug")}'))
        elif "url" in button:
            markup.add(types.InlineKeyboardButton(button.get("cover_text"), url=button.get("url")))
    return markup


def get_button_keyboard(data):
    """Функция создания кнопки."""
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton(data.get("cover_text"), callback_data=f'slug_{data.get("slug")}'))
    return markup


add_data_keyboard = get_back_form_keyboard().add(
    types.InlineKeyboardButton(constants.ADD_DATA_BUTTON_TEXT, callback_data=constants.ADD_FORM_DATA_CALLBACK)
)
cancel_keyboard = get_cancel_keyboard()
submit_keyboard = get_submit_keyboard().add(
    types.InlineKeyboardButton(constants.RECREATE_FORM_BUTTON_TEXT, callback_data=constants.ADD_FORM_DATA_CALLBACK)
)
