from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from src.keyboard import (
    get_user_main_kb,
    get_user_help_kb,
    get_user_products_kb
)

user_router = Router()

# Стартовая команда с основной клавиатурой
@user_router.message(Command("start"))
async def cmd_start(message: Message):
    await message.answer(
        "👋 Добро пожаловать! Выберите действие:",
        reply_markup=get_user_main_kb()
    )

# Обработка кнопки "Помощь"
@user_router.message(F.text == "ℹ Помощь")
async def user_help(message: Message):
    await message.answer(
        "Раздел помощи:",
        reply_markup=get_user_help_kb()
    )

# Обработка кнопки "Товары" (показывает инлайн-кнопки)
@user_router.message(F.text == "📦 Товары")
async def show_products(message: Message):
    await message.answer(
        "Категории товаров:",
        reply_markup=get_user_products_kb()
    )

# Обработка инлайн-кнопок товаров
@user_router.callback_query(F.data.startswith("products_"))
async def products_handler(callback: CallbackQuery):
    action = callback.data.split("_")[1]
    
    if action == "laptops":
        await callback.message.edit_text("💻 Вы выбрали ноутбуки")
    elif action == "phones":
        await callback.message.edit_text("📱 Вы выбрали смартфоны")
    elif action == "back":
        await callback.message.delete()
        await callback.message.answer(
            "Главное меню:",
            reply_markup=get_user_main_kb()
        )
    
    await callback.answer()