from aiogram.types import Message, CallbackQuery
from typing import Union, Optional

ADMIN_IDS = {123456789, 987654321, 1333103477}

async def check_admin_access(
    event: Union[Message, CallbackQuery], 
    silent: bool = False  # Добавляем параметр silent
) -> bool:
    """Проверяет, является ли пользователь админом"""
    user_id = event.from_user.id
    if user_id not in ADMIN_IDS:
        if not silent:  # Проверяем параметр silent
            if isinstance(event, Message):
                await event.answer("⛔ У вас нет прав доступа!")
            elif isinstance(event, CallbackQuery):
                await event.answer("Доступ запрещён!", show_alert=True)
        return False
    return True