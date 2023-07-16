import asyncio

from aiogram import Dispatcher, types
from aiogram.dispatcher import DEFAULT_RATE_LIMIT
from aiogram.dispatcher.handler import CancelHandler, current_handler
from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram.utils.exceptions import Throttled

from app.middleware.constants_middleware import (
    MANY_REQUESTS_MESSAGE,
    THROTTLING_KEY,
    THROTTLING_RATE_LIMIT,
    UNLOCKED_MESSAGE,
)
from core.config import settings


def rate_limit(limit: int, key=None):
    """
    Декоратор для настройки ограничения запросов,
    которые пользователь вводит в бот.
    """

    def decorator(func):
        setattr(func, THROTTLING_RATE_LIMIT, limit)
        if key:
            setattr(func, THROTTLING_KEY, key)
        return func

    return decorator


class ThrottlingMiddleware(BaseMiddleware):
    def __init__(self, rate_limit=DEFAULT_RATE_LIMIT, key_prefix="antiflood_"):
        self.rate_limit = rate_limit
        self.key_prefix = key_prefix
        super(ThrottlingMiddleware, self).__init__()

    def set_limit_and_key(self, handler):
        """
        Функция задаёт предельное значение троттлинга (limit) и key
        для использования этих значений в методе throttle класса Dispatcher.
        """

        # Если обработчик был настроен, получить из хендлера
        # throttling_rate_limit и throttling_key
        if handler:
            limit = getattr(handler, THROTTLING_RATE_LIMIT, self.rate_limit)
            key = getattr(handler, THROTTLING_KEY, f"{self.key_prefix}_{handler.__name__}")
        else:
            limit = self.rate_limit
            key = f"{self.key_prefix}_message"
        return limit, key

    async def on_process_message(self, message: types.Message, data: dict):
        """
        Этот обработчик вызывается, когда dispatcher получает сообщение.
        """

        handler = current_handler.get()
        limit, key = self.set_limit_and_key(handler)
        dispatcher = Dispatcher.get_current()
        try:
            await dispatcher.throttle(key, rate=limit)
        except Throttled as throttled:
            await self.message_throttled(message, throttled)
            raise CancelHandler()

    async def message_throttled(self, message: types.Message, throttled: Throttled):
        """
        Уведомляем пользователя только при первом спаме и уведомляем
        о разблокировке, ссылаясь только на последнее сообщение,
        которое ввёл пользователь во время блокировки.
        """

        handler = current_handler.get()
        _, key = self.set_limit_and_key(handler)
        # Подсчитаем сколько времени осталось до конца блокировки
        delta = throttled.rate - throttled.delta
        # Отправляем пользователя во временную блокировку
        if throttled.exceeded_count <= settings.amount_of_flooding_messages:
            await message.reply(MANY_REQUESTS_MESSAGE)
        await asyncio.sleep(delta)
        dispatcher = Dispatcher.get_current()
        # Проверяем статус блокировки
        throttled_lock_status = await dispatcher.check_key(key)
        # Если текущее сообщение или нажатие кнопки самое последнее,
        # то отправляем сообщение с информацией о конце блокировки
        if throttled_lock_status.exceeded_count == throttled.exceeded_count:
            await message.reply(UNLOCKED_MESSAGE)
