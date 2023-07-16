import enum

from .constants_handlers import HOTLINE_PHONE


class ConstantButtonsData(enum.Enum):
    """
    Данные для постоянных кнопок.
    """

    menu_text = "В главное меню"
    menu_callback_text = "slug_welcome"
    phone_text = "Звонок на горячую линию"
    phone_callback_command = "/phone"
    phone_callback_text = "Нажмите на номер, " "чтобы начать звонок: "

    @classmethod
    def get_phone_text(cls):
        phone_link_url = HOTLINE_PHONE.replace(" ", "")
        phone_link = f'<b><a href="tel:{phone_link_url}">{HOTLINE_PHONE}</a></b>'
        data = cls.phone_callback_text.value + phone_link
        return data
