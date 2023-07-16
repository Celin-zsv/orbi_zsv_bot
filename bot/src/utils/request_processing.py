import logging

from core.aio_client import HttpClient
from core.config import settings
from core.exceptions import ApiClientException


async def parser_request(name):
    """Функция забирает данные из БД и возвращает запрос."""
    async with HttpClient() as client:
        # If no request with this name return 404 and it's acceptable error_code.
        # The new request will be created.
        return await client.get(f"{settings.api_url}requests/{name}/", (200, 404))


async def post_request(title):
    """Функция создает новый запрос со статусом 'Не обработан' в БД."""
    async with HttpClient() as client:
        response = await client.post(
            f"{settings.api_url}request/",
            {"request": title, "processing_status": "WAITING"},
        )
    return response.get("id")


async def up_counter(id):
    """Функция увеличивает счетчик запроса на 1."""
    async with HttpClient() as client:
        await client.patch(f"{settings.api_url}request_update/{id}/")


async def get_request_data(name):
    """
    Функция забирает из БД id запроса,
    text и buttons, привязанного к нему текста.
    Если получена ошибка от API, то возвращает None и логирует ошибку.
    """
    try:
        request = await parser_request(name)
    except ApiClientException as error:
        logging.error(f"An API client exception occurred: {str(error)}")
        return None
    request_id = request.get("id")
    try:
        request_text = request.get("text")
        buttons_slug = request_text.get("button_slug")
        buttons_url = request_text.get("button_url")
        text = request_text.get("text")
        buttons = {
            "ButtonSlug": buttons_slug,
            "ButtonUrl": buttons_url,
        }
    except AttributeError:
        logging.info(f"Request {name} has no text or buttons.")
        text = None
        buttons = None
    return request_id, text, buttons
