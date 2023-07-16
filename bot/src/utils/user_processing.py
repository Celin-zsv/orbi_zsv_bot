from core.aio_client import HttpClient
from core.config import settings


async def parser_user():
    """Функция забирает данные из БД и возвращает список пользователей."""
    async with HttpClient() as client:
        return await client.get(f"{settings.api_url}users/")


async def post_user(user_id):
    """Функция создает нового пользователя в БД."""
    async with HttpClient() as client:
        await client.post(f"{settings.api_url}user/", {"user_id": user_id})


async def update_user(user_id, id):
    """Функция редактирует пользователя, добавляя к нему запрос."""
    async with HttpClient() as client:
        await client.patch(f"{settings.api_url}user_update/{user_id}/", {"requests": id})


async def check_user(user_id):
    """Функция ищет пользователя в списке возвращенном parser_user."""
    users = await parser_user()
    return str(user_id) in tuple(i["user_id"] for i in users)
