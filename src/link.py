from aiogram.types import Message, CallbackQuery
from typing import Union
from src.config import settings


async def check_admin_access(
    event: Union[Message, CallbackQuery],
    silent: bool = False,  # Добавляем параметр silent
) -> bool:
    """Проверяет, является ли пользователь админом"""
    user_id = event.from_user.id
    if user_id not in settings.ADMIN_IDS:
        if not silent:  # Проверяем параметр silent
            if isinstance(event, Message):
                await event.answer("⛔ У вас нет прав доступа!")
            elif isinstance(event, CallbackQuery):
                await event.answer("Доступ запрещён!", show_alert=True)
        return False
    return True
