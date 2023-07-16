from aiogram.types import CallbackQuery, InlineKeyboardMarkup, Message

from app.orbi_bot import dp


async def send_or_edit_message(
    text: str,
    buttons: InlineKeyboardMarkup,
    callback_query: CallbackQuery = None,
    message: Message = None,
    parse_mode: str = "HTML",
) -> None:
    """Processing html markup messages."""

    text = text.replace("<br />", "\n")

    if message:
        await message.answer(text, reply_markup=buttons, parse_mode=parse_mode, disable_web_page_preview=True)
    elif callback_query:
        await dp.bot.edit_message_text(
            text,
            chat_id=callback_query.message.chat.id,
            message_id=callback_query.message.message_id,
            reply_markup=buttons,
            parse_mode=parse_mode,
            disable_web_page_preview=True,
        )
