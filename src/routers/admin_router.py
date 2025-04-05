from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from  src.keyboard  import (
    get_main_admin_kb,
    get_location_kb,
    get_inline_kb,
    get_url_kb,
    get_user_start_kb
)

admin_router = Router()


# Приветствие + клавиатура со стартом
@admin_router.message(Command("start"))
async def user_start(message: Message):
    await message.answer(
        "👋 Добро пожаловать! Вот ваше меню:",
        reply_markup=get_user_start_kb()  # Подключаем клавиатуру
    )

# ===== 1. REPLY-КНОПКИ =====
@admin_router.message(Command("admin"))
async def admin_panel(message: Message):
    await message.answer(
        "🛡️ Админ-панель",
        reply_markup=get_main_admin_kb()  # Основная клавиатура
    )

@admin_router.message(F.text == "Кнопка 1")
async def button1_handler(message: Message):
    await message.answer("Вы нажали Кнопку 1")

@admin_router.message(F.text == "Отправить локацию")
async def request_location(message: Message):
    await message.answer(
        "Отправьте вашу локацию:",
        reply_markup=get_location_kb()
    )

# ===== 2. INLINE-КНОПКИ =====
@admin_router.message(Command("inline"))
async def show_inline_kb(message: Message):
    await message.answer(
        "Выберите действие:",
        reply_markup=get_inline_kb()
    )

@admin_router.callback_query(F.data.startswith("btn"))
async def inline_button_handler(callback: CallbackQuery):
    btn_number = callback.data.replace("btn", "")
    await callback.message.edit_text(f"Нажата кнопка {btn_number}")
    await callback.answer()

# ===== 3. URL-КНОПКА =====
@admin_router.message(Command("url"))
async def show_url_button(message: Message):
    await message.answer(
        "Перейти на сайт:",
        reply_markup=get_url_kb()
    )