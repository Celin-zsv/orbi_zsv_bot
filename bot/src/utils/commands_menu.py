from aiogram import Dispatcher

from utils.utils_constants import BOT_COMMANDS


async def set_bot_commands(dp: Dispatcher):
    """Define bot commands menu."""
    await dp.bot.set_my_commands(commands=BOT_COMMANDS)
