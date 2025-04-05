from aiogram.types import (
    ReplyKeyboardMarkup, KeyboardButton,
    InlineKeyboardMarkup, InlineKeyboardButton
)

def get_user_main_kb():
    """Основная клавиатура пользователя"""
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📝 Подать заявку")],
            [KeyboardButton(text="📚 Выбрать тематику"), KeyboardButton(text="🔕 Отключить уведомления")],
            [KeyboardButton(text="📰 Посмотреть статьи"), KeyboardButton(text="ℹ Помощь")]
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

def get_themes_kb():
    """Инлайн-кнопки для выбора тематики"""
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Технологии", callback_data="theme_tech")],
            [InlineKeyboardButton(text="Наука", callback_data="theme_science")],
            [InlineKeyboardButton(text="Искусство", callback_data="theme_art")],
            [InlineKeyboardButton(text="🔙 Назад", callback_data="theme_back")]
        ]
    )

def get_articles_kb():
    """Инлайн-кнопки для статей"""
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Последние статьи", callback_data="articles_latest")],
            [InlineKeyboardButton(text="Популярные статьи", callback_data="articles_popular")],
            [InlineKeyboardButton(text="🔙 Назад", callback_data="articles_back")]
        ]
    )

def get_article_url_kb(url: str):
    """Кнопка для перехода на сайт со статьёй"""
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🔗 Перейти на сайт", url=url)]
        ]
    )

def get_notifications_kb():
    """Клавиатура для управления уведомлениями"""
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🔕 Отключить уведомления", callback_data="notifications_off")],
            [InlineKeyboardButton(text="🔔 Включить уведомления", callback_data="notifications_on")],
            [InlineKeyboardButton(text="🔙 Назад", callback_data="notifications_back")]
        ]
    )