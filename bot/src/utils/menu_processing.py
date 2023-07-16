from core.aio_client import HttpClient
from core.config import settings


async def parser_slug_text_with_buttons(text_slug):
    """Функция забирает данные из БД и возвращает текст и список кнопок."""
    async with HttpClient() as client:
        data = await client.get(f"{settings.api_url}texts/{text_slug}/")
    text = data.get("text")
    buttons = {
        "ButtonSlug": data.get("button_slug"),
        "ButtonUrl": data.get("button_url"),
    }
    return text, buttons


async def parser_main_button():
    """Функция забирает данные из БД и возвращает кнопку в главное меню."""
    async with HttpClient() as client:
        data = await client.get(f"{settings.api_url}buttons/")
    button_slug = data.get("ButtonSlug")
    for button in button_slug:
        if button.get("is_main"):
            return button
