from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from typing import Optional
import logging
from src.keyboard_admin import (
    get_admin_main_kb,
    get_admin_articles_kb,
    get_admin_article_actions_kb,
    get_admin_requests_kb,
    get_admin_request_actions_kb
)
from src.repository.db_helper import async_session

from src.service.user_service import UserService  # Импорт проверки прав

admin_router = Router()

async def safe_extract_id(data: str, prefix: str) -> Optional[int]:
    """Безопасное извлечение ID из callback данных"""
    try:
        return int(data.replace(prefix, ""))
    except (ValueError, AttributeError) as e:
        logging.error(f"Error extracting ID from {data}: {e}")
        return None

async def handle_admin_errors(event: Message | CallbackQuery, 
                           error_msg: str = "Произошла ошибка"):
    """Обработка ошибок для админских действий"""
    if isinstance(event, Message):
        await event.answer("⚠️ " + error_msg)
    elif isinstance(event, CallbackQuery):
        await event.answer("⚠️ " + error_msg, show_alert=True)
        await event.message.edit_reply_markup()

async def check_admin_access(event: Message | CallbackQuery) -> bool:
    """Проверяет права администратора через UserService"""
    try:
        user_id = event.from_user.id
        async with async_session() as session:
            user_service = UserService(session)
            return await user_service.is_admin(user_id)
    except Exception as e:
        logging.error(f"Admin check error: {e}")
        return False

# ========== Обработчики сообщений ==========
@admin_router.message(Command("admin"))
async def admin_start(message: Message):
    if not await check_admin_access(message):
        await handle_admin_errors(message, "Доступ запрещён")
        return
    
    try:
        await message.answer(
            "👑 Панель администратора:",
            reply_markup=get_admin_main_kb()
        )
    except Exception as e:
        logging.error(f"Error in admin_start: {e}")
        await handle_admin_errors(message, "Ошибка доступа к панели")

@admin_router.message(F.text == "📝 Посмотреть статьи")
async def show_articles(message: Message):
    if not await check_admin_access(message):
        await handle_admin_errors(message, "Доступ запрещён")
        return
    
    try:
        articles = [
            {"id": 1, "title": "Статья 1"},
            {"id": 2, "title": "Статья 2"}
        ]
        
        await message.answer(
            "📚 Список статей:",
            reply_markup=get_admin_articles_kb(articles)
        )
    except Exception as e:
        logging.error(f"Error in show_articles: {e}")
        await handle_admin_errors(message, "Ошибка загрузки статей")

# ========== Обработчики callback-запросов ==========
@admin_router.callback_query(F.data.startswith("admin_article_"))
async def handle_article(callback: CallbackQuery):
    if not await check_admin_access(callback):
        await handle_admin_errors(callback, "Доступ запрещён")
        return
    
    try:
        article_id = await safe_extract_id(callback.data, "admin_article_")
        if not article_id:
            raise ValueError("Invalid article ID")
        
        await callback.message.edit_text(
            f"Управление статьёй ID: {article_id}",
            reply_markup=get_admin_article_actions_kb(article_id)
        )
        await callback.answer()
    except Exception as e:
        logging.error(f"Error in handle_article: {e}")
        await handle_admin_errors(callback, "Ошибка обработки статьи")

# ========== Навигационные обработчики ==========
@admin_router.callback_query(F.data == "admin_back_to_main")
async def back_to_main(callback: CallbackQuery):
    if not await check_admin_access(callback):
        await handle_admin_errors(callback, "Доступ запрещён")
        return
    
    try:
        await callback.message.edit_text(
            "👑 Панель администратора:",
            reply_markup=get_admin_main_kb()
        )
        await callback.answer()
    except Exception as e:
        logging.error(f"Error in back_to_main: {e}")
        await handle_admin_errors(callback, "Ошибка навигации")