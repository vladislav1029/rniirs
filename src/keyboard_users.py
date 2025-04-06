from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from src.models import Article


def get_user_main_kb():
    """Основная клавиатура пользователя"""
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📝 Подать заявку")],
            [
                KeyboardButton(text="📚 Выбрать тематику"),
                KeyboardButton(text="🔕 Отключить уведомления"),
            ],
            [
                KeyboardButton(text="📰 Посмотреть статьи"),
                KeyboardButton(text="ℹ Помощь"),
            ],
        ],
        resize_keyboard=True,
        one_time_keyboard=False,
    )


def get_privacy_selection_kb():
    builder = InlineKeyboardBuilder()
    builder.button(text="🔒 Приватный", callback_data="privacy_private")
    builder.button(text="🌍 Публичный", callback_data="privacy_public")
    return builder.as_markup()


def get_catalog_actions_kb(catalog_id: int):
    builder = InlineKeyboardBuilder()
    builder.button(text="✏️ Переименовать", callback_data=f"edit_catalog_{catalog_id}")
    builder.button(text="❌ Удалить", callback_data=f"delete_catalog_{catalog_id}")
    builder.button(text="🔙 К списку", callback_data="my_catalogs")
    builder.adjust(1)
    return builder.as_markup()


def get_catalog_confirm_kb(catalog_id: int):
    builder = InlineKeyboardBuilder()
    builder.button(text="✅ Да", callback_data=f"confirm_delete_{catalog_id}")
    builder.button(text="❌ Нет", callback_data=f"view_catalog_{catalog_id}")
    return builder.as_markup()


def get_back_to_catalogs_kb(catalog_id: int):
    builder = InlineKeyboardBuilder()
    builder.button(text="🔙 Отмена", callback_data=f"view_catalog_{catalog_id}")
    return builder.as_markup()


def get_catalog_articles_kb(catalog_id: int):
    builder = InlineKeyboardBuilder()
    builder.button(
        text="🗑️ Удалить статью", callback_data=f"delete_article_menu_{catalog_id}"
    )   
    builder.button(text="🔙 К каталогу", callback_data=f"view_catalog_{catalog_id}")
    builder.adjust(1)
    return builder.as_markup()


def get_public_catalog_kb(catalog_id: int):
    builder = InlineKeyboardBuilder()
    builder.button(
        text="⭐ Добавить в избранное", callback_data=f"fav_catalog_{catalog_id}"
    )
    builder.button(text="🔍 Поиск других", callback_data="search_public")
    builder.adjust(1)
    return builder.as_markup()


def get_article_delete_kb(articles: list[Article]):
    builder = InlineKeyboardBuilder()
    for article in articles:
        builder.button(
            text=f"❌ {article.title[:15]}",
            callback_data=f"delete_article_{article.id}",
        )
    builder.button(text="🔙 Назад", callback_data="my_catalogs")
    builder.adjust(2)
    return builder.as_markup()
