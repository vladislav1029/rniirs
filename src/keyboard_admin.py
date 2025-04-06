from aiogram.types import (
    ReplyKeyboardMarkup, KeyboardButton,
    InlineKeyboardMarkup, InlineKeyboardButton
)

def get_admin_main_kb():
    """Основная клавиатура админа"""
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📝 Посмотреть статьи")],
            [KeyboardButton(text="✏ Редакция статьи")],
            [KeyboardButton(text="📋 Посмотреть заявки пользователей")]
        ],
        resize_keyboard=True,
        one_time_keyboard=False
    )

def get_admin_articles_kb(articles: list):
    """Инлайн-кнопки для статей (динамические)"""
    buttons = []
    for article in articles:
        buttons.append([InlineKeyboardButton(
            text=f"📄 {article['title']}",
            callback_data=f"admin_article_{article['id']}"
        )])
    
    buttons.append([InlineKeyboardButton(
        text="🔙 Назад",
        callback_data="admin_back_to_main"
    )])
    
    return InlineKeyboardMarkup(inline_keyboard=buttons)

def get_admin_article_actions_kb(article_id: int):
    """Действия со статьёй"""
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="✏ Редактировать", callback_data=f"admin_edit_{article_id}"),
                InlineKeyboardButton(text="🗑 Удалить", callback_data=f"admin_delete_{article_id}")
            ],
            [InlineKeyboardButton(text="🔙 Назад к статьям", callback_data="admin_back_to_articles")]
        ]
    )

def get_admin_requests_kb(requests: list):
    """Кнопки для заявок пользователей"""
    buttons = []
    for req in requests:
        buttons.append([InlineKeyboardButton(
            text=f"📌 {req['user_name']} - {req['type']}",
            callback_data=f"admin_request_{req['id']}"
        )])
    
    buttons.append([InlineKeyboardButton(
        text="🔙 Назад",
        callback_data="admin_back_to_main"
    )])
    
    return InlineKeyboardMarkup(inline_keyboard=buttons)

def get_admin_request_actions_kb(request_id: int):
    """Действия с заявкой"""
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="✅ Одобрить", callback_data=f"admin_approve_{request_id}"),
                InlineKeyboardButton(text="❌ Отклонить", callback_data=f"admin_reject_{request_id}")
            ],
            [InlineKeyboardButton(text="🔙 Назад к заявкам", callback_data="admin_back_to_requests")]
        ]
    )