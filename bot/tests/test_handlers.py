from unittest.mock import AsyncMock

from aiohttp import ClientConnectionError

from app import get_charity_keyboard
from app.handlers import message
from app.handlers.constant_buttons import contact_phone, welcome_menu
from app.handlers.forms.keyboards import add_buttons, get_menu_keyboard
from core.config import settings


async def test_send_welcome(monkeypatch):
    test_buttons = {"ButtonUrl": [{"url": "https://orbifond.ru/", "cover_text": "test_cover_text"}]}
    test_markup = get_menu_keyboard(test_buttons)
    add_buttons([contact_phone], test_markup)

    async def mock_parser_slug_text_with_buttons(text_slug):
        return ["test_text", test_buttons]

    mock_markup = AsyncMock()
    monkeypatch.setattr(message, "parser_slug_text_with_buttons", mock_parser_slug_text_with_buttons)
    monkeypatch.setattr(message, "send_or_edit_message", mock_markup)
    welcome_message = AsyncMock()
    await message.send_welcome(welcome_message)
    mock_markup.assert_called_with(text="test_text", buttons=test_markup, message=welcome_message)


async def test_send_welcome_error(monkeypatch):
    async def mock_parser_slug_text_with_buttons_error(text_id):
        raise ClientConnectionError

    monkeypatch.setattr(message, "parser_slug_text_with_buttons", mock_parser_slug_text_with_buttons_error)

    welcome_message = AsyncMock()
    await message.send_welcome(welcome_message)
    welcome_message.answer.assert_called_with(
        "Извините, бот временно недоступен, " "но можно воспользоваться сайтом ОРБИ: " f"<a>{settings.spare_url}</a>",
        parse_mode="HTML",
        reply_markup=add_buttons([contact_phone]),
    )


async def test_form(monkeypatch):
    async def mock_set():
        return None

    monkeypatch.setattr(message.FormStatesGroup.set_form, "set", mock_set)
    form_message = AsyncMock()
    await message.form(form_message)
    buttons = get_charity_keyboard()
    markup = add_buttons([welcome_menu, contact_phone], buttons)
    form_message.answer.assert_called_with("Как бы Вы хотели помочь?", reply_markup=markup)
