from datetime import datetime

from aiogram import types
from aiogram.dispatcher.filters import BoundFilter


class DateFilter(BoundFilter):
    """
    Check if date is in future or not
    """

    key = "future_date"

    def __init__(self, future_date: bool):
        self.in_future = future_date

    async def check(self, obj: types.Message):
        try:
            date = datetime.strptime(obj.text, "%d.%m.%Y")
            if date <= datetime.now():
                return self.in_future is False
            return self.in_future is True
        except ValueError:
            return True
