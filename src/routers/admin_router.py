from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from src.keyboard import (
    get_admin_main_kb,
    get_admin_articles_kb,
    get_admin_article_actions_kb,
    get_admin_requests_kb,
    get_admin_request_actions_kb
)

# ID админов (можно вынести в конфиг или БД)
ADMIN_IDS = {123456789, 987654321}

admin_router = Router()

# Проверка на админа
async def is_admin(user_id: int) -> bool:
    return user_id in ADMIN_IDS

# Стартовая команда с проверкой админа
@admin_router.message(Command("admin"))
async def admin_start(message: Message):
    if not await is_admin(message.from_user.id):
        await message.answer("⛔ У вас нет прав доступа!")
        return
    
    await message.answer(
        "👑 Панель администратора:",
        reply_markup=get_admin_main_kb()
    )

# Обработка кнопки "Посмотреть статьи"
@admin_router.message(F.text == "📝 Посмотреть статьи")
async def show_articles(message: Message):
    if not await is_admin(message.from_user.id):
        return
    
    # Здесь должна быть логика получения статей из БД
    articles = [
        {"id": 1, "title": "Статья 1"},
        {"id": 2, "title": "Статья 2"}
    ]
    
    await message.answer(
        "📚 Список статей:",
        reply_markup=get_admin_articles_kb(articles)
    )

# Обработка кнопки "Редакция статьи"
@admin_router.message(F.text == "✏ Редакция статьи")
async def edit_article(message: Message):
    if not await is_admin(message.from_user.id):
        return
    
    await message.answer(
        "Введите ID статьи для редактирования:",
        reply_markup=get_admin_main_kb()
    )

# Обработка кнопки "Посмотреть заявки"
@admin_router.message(F.text == "📋 Посмотреть заявки пользователей")
async def show_requests(message: Message):
    if not await is_admin(message.from_user.id):
        return
    
    # Логика получения заявок из БД
    requests = [
        {"id": 1, "user_name": "User1", "type": "Регистрация"},
        {"id": 2, "user_name": "User2", "type": "Поддержка"}
    ]
    
    await message.answer(
        "📨 Заявки пользователей:",
        reply_markup=get_admin_requests_kb(requests)
    )

# Обработка инлайн-кнопок статей
@admin_router.callback_query(F.data.startswith("admin_article_"))
async def handle_article(callback: CallbackQuery):
    if not await is_admin(callback.from_user.id):
        return
    
    article_id = int(callback.data.split("_")[-1])
    await callback.message.edit_text(
        f"Управление статьёй ID: {article_id}",
        reply_markup=get_admin_article_actions_kb(article_id)
    )
    await callback.answer()

# Обработка действий со статьёй
@admin_router.callback_query(F.data.startswith("admin_edit_"))
async def edit_article_action(callback: CallbackQuery):
    article_id = int(callback.data.split("_")[-1])
    await callback.message.answer(f"Редактирование статьи ID: {article_id}")
    await callback.answer()

@admin_router.callback_query(F.data.startswith("admin_delete_"))
async def delete_article_action(callback: CallbackQuery):
    article_id = int(callback.data.split("_")[-1])
    await callback.message.answer(f"Удаление статьи ID: {article_id}")
    await callback.answer()

# Обработка заявок
@admin_router.callback_query(F.data.startswith("admin_request_"))
async def handle_request(callback: CallbackQuery):
    request_id = int(callback.data.split("_")[-1])
    await callback.message.edit_text(
        f"Заявка ID: {request_id}\nВыберите действие:",
        reply_markup=get_admin_request_actions_kb(request_id)
    )
    await callback.answer()

# Обработка действий с заявками
@admin_router.callback_query(F.data.startswith("admin_approve_"))
async def approve_request(callback: CallbackQuery):
    request_id = int(callback.data.split("_")[-1])
    await callback.message.answer(f"Заявка {request_id} одобрена!")
    await callback.answer()

@admin_router.callback_query(F.data.startswith("admin_reject_"))
async def reject_request(callback: CallbackQuery):
    request_id = int(callback.data.split("_")[-1])
    await callback.message.answer(f"Заявка {request_id} отклонена!")
    await callback.answer()

# Навигационные кнопки
@admin_router.callback_query(F.data == "admin_back_to_main")
async def back_to_main(callback: CallbackQuery):
    await callback.message.edit_text(
        "👑 Панель администратора:",
        reply_markup=get_admin_main_kb()
    )
    await callback.answer()

@admin_router.callback_query(F.data == "admin_back_to_articles")
async def back_to_articles(callback: CallbackQuery):
    articles = [
        {"id": 1, "title": "Статья 1"},
        {"id": 2, "title": "Статья 2"}
    ]
    await callback.message.edit_text(
        "📚 Список статей:",
        reply_markup=get_admin_articles_kb(articles)
    )
    await callback.answer()