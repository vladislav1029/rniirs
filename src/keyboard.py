from aiogram.types import (
    ReplyKeyboardMarkup, KeyboardButton,
    InlineKeyboardMarkup, InlineKeyboardButton
)

def get_user_main_kb():
    """Основная клавиатура пользователя с кнопкой Start"""
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="/start")],  # Стартовая кнопка сверху
            [KeyboardButton(text="ℹ Помощь"), KeyboardButton(text="📦 Товары")],
            [KeyboardButton(text="📞 Контакты")]
        ],
        resize_keyboard=True,
        one_time_keyboard=False
    )

def get_user_help_kb():
    """Клавиатура для раздела помощи"""
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="❓ Частые вопросы")],
            [KeyboardButton(text="📞 Техподдержка")],
            [KeyboardButton(text="🔙 Назад")]
        ],
        resize_keyboard=True
    )

def get_user_products_kb():
    """Инлайн-кнопки для товаров"""
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="💻 Ноутбуки", callback_data="products_laptops")],
            [InlineKeyboardButton(text="📱 Смартфоны", callback_data="products_phones")],
            [InlineKeyboardButton(text="🔙 Назад", callback_data="products_back")]
        ]
    )

def get_user_start_kb():
    """Клавиатура для пользователя с кнопкой Старт"""
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="/start")],  # Кнопка старта сверху
            [KeyboardButton(text="Кнопка 1"), KeyboardButton(text="Кнопка 2")],
            [KeyboardButton(text="Кнопка 3")]
        ],
        resize_keyboard=True,
        one_time_keyboard=False  # Чтобы клавиатура не скрывалась
    )
# ===== REPLY-КЛАВИАТУРЫ =====
def get_main_admin_kb():
    """Основная клавиатура админа"""
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Кнопка 1"), KeyboardButton(text="Кнопка 2")],
            [KeyboardButton(text="Кнопка 3")]
        ],
        resize_keyboard=True,
        one_time_keyboard=True
    )

def get_location_kb():
    """Клавиатура с запросом локации"""
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Отправить локацию", request_location=True)]
        ],
        resize_keyboard=True
    )

# ===== INLINE-КЛАВИАТУРЫ =====
def get_inline_kb():
    """Инлайн-кнопки"""
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Кнопка 1", callback_data="btn1")],
            [InlineKeyboardButton(text="Кнопка 2", callback_data="btn2")],
            [
                InlineKeyboardButton(text="Кнопка 3", callback_data="btn3"),
                InlineKeyboardButton(text="Кнопка 4", callback_data="btn4")
            ]
        ]
    )

def get_url_kb():
    """Кнопка с URL"""
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Открыть сайт", url="https://example.com")]
        ]
    )