"""Bot mods."""
from aiogram import Bot, Dispatcher, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.utils.executor import start_webhook

from app.middleware.antispam import ThrottlingMiddleware
from core.config import settings
from core.logger import logging
from filters.date import DateFilter
from utils.commands_menu import set_bot_commands

bot = Bot(token=settings.telegram_api_token)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
dp.middleware.setup(ThrottlingMiddleware())
dp.filters_factory.bind(DateFilter, event_handlers=[dp.message_handlers])
WEBHOOK_URL = f"{settings.webhook_host}{settings.webhook_path}"


async def on_startup(dp):
    """Set webhook and commands menu."""
    await set_bot_commands(dp)
    webhook_info = await bot.get_webhook_info()
    if webhook_info.url != WEBHOOK_URL:
        await bot.set_webhook(url=WEBHOOK_URL)
        webhook_info = await bot.get_webhook_info()


async def on_shutdown(dp):
    """Delete webhook."""
    logging.warning("Shutting down..")
    await bot.delete_webhook()
    await dp.storage.close()
    await dp.storage.wait_closed()
    logging.warning("Bye!")


def run_polling():
    """Start polling mode."""
    executor.start_polling(dp, on_startup=set_bot_commands)


def run_webhooks():
    """Start webhook mode."""
    start_webhook(
        dispatcher=dp,
        webhook_path=settings.webhook_path,
        on_startup=on_startup,
        on_shutdown=on_shutdown,
        port="80",
    )
