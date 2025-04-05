from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

# Простая клавиатура
keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Кнопка 1"), KeyboardButton(text="Кнопка 2")],
        [KeyboardButton(text="Кнопка 3")]
    ],
    resize_keyboard=True,  # Подгоняет размер кнопок
    one_time_keyboard=True  # Скрывает после нажатия
)

# Кнопка с запросом локации
location_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Отправить локацию", request_location=True)]
    ],
    resize_keyboard=True
)

# Кнопка с запросом контакта
contact_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Отправить контакт", request_contact=True)]
    ],
    resize_keyboard=True
)
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# Простые inline-кнопки
inline_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Кнопка 1", callback_data="btn1")],
        [InlineKeyboardButton(text="Кнопка 2", callback_data="btn2")],
        [
            InlineKeyboardButton(text="Кнопка 3", callback_data="btn3"),
            InlineKeyboardButton(text="Кнопка 4", callback_data="btn4")
        ]
    ]
)

# Кнопка с URL
url_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Открыть сайт", url="https://example.com")]
    ]
)

# Кнопка для перехода в другой чат
chat_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Перейти в чат", url="tg://resolve?domain=username")]
    ]
)