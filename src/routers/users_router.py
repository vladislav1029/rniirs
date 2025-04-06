from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from src.keyboard_users import get_user_main_kb, get_user_help_kb  # Импорт клавиатур

# Импорт проверки прав
from src.repository.db_helper import async_session

from src.schemas import UserCreate
from src.service.user_service import UserService  # Импорт проверки прав

user_router = Router()


@user_router.message(Command("start"))
async def cmd_start(message: Message):
    async with async_session() as session:
        # Работа с пользователями
        user = UserService(session)

        new_user = await user.create_user(UserCreate(id=message.from_user.id))

        is_admin = await user.is_admin(message.from_user.id)

    if is_admin:
        from .admin_router import admin_start  # Ленивый импорт

        await admin_start(message)
    else:
        await message.answer("👋 Добро пожаловать!", reply_markup=get_user_main_kb())


# Обработка кнопки "Помощь"
@user_router.message(F.text == "ℹ Помощь")
async def user_help(message: Message):
    await message.answer("Раздел помощи:", reply_markup=get_user_help_kb())


# Обработка кнопки "Подать заявку" (заглушка)
@user_router.message(F.text == "📝 Подать заявку")
async def submit_application(message: Message):
    await message.answer("⏳ Функция подачи заявки в разработке")


# Обработка кнопки "Выбрать тематику"
@user_router.message(F.text == "📚 Выбрать тематику")
async def choose_theme(message: Message):
    await message.answer(
        "Выберите интересующую тематику:", reply_markup=get_themes_kb()
    )


# Обработка кнопки "Отключить уведомления"
@user_router.message(F.text == "🔕 Отключить уведомления")
async def manage_notifications(message: Message):
    await message.answer(
        "Управление уведомлениями:", reply_markup=get_notifications_kb()
    )


# Обработка кнопки "Посмотреть статьи"
@user_router.message(F.text == "📰 Посмотреть статьи")
async def view_articles(message: Message):
    await message.answer("Выберите тип статей:", reply_markup=get_articles_kb())


# Обработка инлайн-кнопок тематик
@user_router.callback_query(F.data.startswith("theme_"))
async def themes_handler(callback: CallbackQuery):
    action = callback.data.split("_")[1]

    if action == "tech":
        await callback.message.edit_text("Вы выбрали тематику: Технологии")
    elif action == "science":
        await callback.message.edit_text("Вы выбрали тематику: Наука")
    elif action == "art":
        await callback.message.edit_text("Вы выбрали тематику: Искусство")
    elif action == "back":
        await callback.message.delete()
        await callback.message.answer("Главное меню:", reply_markup=get_user_main_kb())

    await callback.answer()


# Обработка инлайн-кнопок статей
@user_router.callback_query(F.data.startswith("articles_"))
async def articles_handler(callback: CallbackQuery):
    action = callback.data.split("_")[1]

    if action == "latest":
        # Пример сообщения со статьёй и кнопкой перехода
        article_text = "📰 Последняя статья:\n\nЗаголовок: Новые технологии в IT\n\nОписание: Обзор последних тенденций..."
        await callback.message.edit_text(
            article_text,
            reply_markup=get_article_url_kb("https://example.com/latest-article"),
        )
    elif action == "popular":
        article_text = "📰 Популярная статья:\n\nЗаголовок: Топ-10 научных открытий\n\nОписание: Самые важные открытия года..."
        await callback.message.edit_text(
            article_text,
            reply_markup=get_article_url_kb("https://example.com/popular-article"),
        )
    elif action == "back":
        await callback.message.delete()
        await callback.message.answer("Главное меню:", reply_markup=get_user_main_kb())

    await callback.answer()


# Обработка инлайн-кнопок уведомлений
@user_router.callback_query(F.data.startswith("notifications_"))
async def notifications_handler(callback: CallbackQuery):
    action = callback.data.split("_")[1]

    if action == "off":
        await callback.message.edit_text("🔕 Уведомления отключены")
    elif action == "on":
        await callback.message.edit_text("🔔 Уведомления включены")
    elif action == "back":
        await callback.message.delete()
        await callback.message.answer("Главное меню:", reply_markup=get_user_main_kb())

    await callback.answer()


# Обработка кнопки "Назад" в обычных клавиатурах
@user_router.message(F.text == "🔙 Назад")
async def back_to_main(message: Message):
    await message.answer("Главное меню:", reply_markup=get_user_main_kb())
