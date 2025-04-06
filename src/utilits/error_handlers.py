import logging
from aiogram.types import Message, CallbackQuery


async def handle_user_errors(
    event: Message | CallbackQuery, error_msg: str = "Произошла ошибка"
):
    """Обработка ошибок для пользовательских действий"""
    error_text = f"⚠️ {error_msg}"

    try:
        if isinstance(event, Message):
            await event.answer(error_text)
        elif isinstance(event, CallbackQuery):
            await event.answer(error_text, show_alert=True)
            await event.message.edit_reply_markup()

    except Exception as e:
        logging.error(f"Error handling error: {e}")
