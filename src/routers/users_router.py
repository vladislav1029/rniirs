import logging
from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command, StateFilter
from aiogram.fsm.state import StatesGroup, State
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.utils.markdown import hbold
from src.models import Article, PrivateEnum
from src.repository.article_repository import ArticleRepository
from src.repository.catalog_repository import CatalogRepository
from src.schemas import CatalogCreate, UserCreate
from src.keyboard_users import (
    get_catalog_actions_kb,
    get_catalog_articles_kb,
    get_catalog_confirm_kb,
    get_back_to_catalogs_kb,
    get_privacy_selection_kb,
    get_public_catalog_kb,
    get_user_main_kb,
)
from src.fsms import CatalogStates
from src.repository.db_helper import async_session
from src.service.user_service import UserService
from src.utilits.error_handlers import handle_user_errors

user_router = Router()
log = logging.Logger(__name__)


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
        
        start_text = (
        f"📚 {hbold('Добро пожаловать в CatalogBot!')}\n\n"
        "✨ Доступные команды:\n"
        "/start - Главное меню\n"
        "/help - Помощь по боту\n"
        "/create_catalog - Создать новый каталог\n"
        "/my_catalogs - Мои каталоги\n"
        "/search_public - Поиск публичных каталогов\n\n"
        "⚡ Быстрые действия через кнопки меню!"
        )
        await message.answer(
        start_text,
        reply_markup=get_user_main_kb(),
        parse_mode="HTML"
    )
    
    

# Хендлер для добавления статей через reply
@user_router.message(F.reply_to_message)
async def add_article_reply(message: Message):
    try:
        original_text = message.reply_to_message.text
        if "Управление каталогом" not in original_text:
            return
            
        catalog_id = int(original_text.split("ID: ")[1].split("\n")[0])
        
        async with async_session() as session:
            # Проверка прав доступа
            repo = CatalogRepository(session)
            catalog = await repo.get_catalog_by_id(catalog_id)
            
            if catalog.user_id != message.from_user.id:
                await message.answer("❌ Нет прав для редактирования этого каталога")
                return
            ArticleRepository
            article_repo = ArticleRepository(session)
            new_article = Article(
                title="Новая статья",
                description=message.text,
                catalog_id=catalog_id
            )
            session.add(new_article)
            await session.commit()
            
            await message.answer(
                "✅ Статья успешно добавлена!",
                reply_markup=get_catalog_articles_kb(catalog_id)
            )
            
    except Exception as e:
        logging.error(f"Add article error: {e}")
        await message.answer("⚠️ Ошибка добавления статьи")

# Поиск публичных каталогов
@user_router.message(Command("search_public"))
async def search_public_catalogs(message: Message):
    try:
        async with async_session() as session:
            repo = CatalogRepository(session)
            public_catalogs = await repo.get_public_catalogs()
            
            if not public_catalogs:
                await message.answer("🔍 Публичные каталоги не найдены")
                return
            
            builder = InlineKeyboardBuilder()
            for catalog in public_catalogs:
                builder.button(
                    text=f"📁 {catalog.title} ({catalog.user_id})",
                    callback_data=f"view_public_catalog_{catalog.id}"
                )
            builder.adjust(1)
            
            await message.answer(
                "🌍 Публичные каталоги:",
                reply_markup=builder.as_markup()
            )
            
    except Exception as e:
        logging.error(f"Public search error: {e}")
        await message.answer("⚠️ Ошибка поиска")

# Удаление статей
@user_router.callback_query(F.data.startswith("delete_article_"))
async def delete_article(callback: CallbackQuery):
    try:
        article_id = int(callback.data.split("_")[-1])
        
        async with async_session() as session:
            article_repo = ArticleRepository(session)
            article = await article_repo.get_article(article_id)
            
            if not article:
                await callback.answer("❌ Статья не найдена")
                return
                
            # Проверка прав через каталог
            catalog_repo = CatalogRepository(session)
            catalog = await catalog_repo.get_catalog_by_id(article.catalog_id)
            
            if catalog.user_id != callback.from_user.id:
                await callback.answer("❌ Нет прав на удаление")
                return
            
            await article_repo.delete_article(article_id)
            await callback.message.edit_text(
                text=f"✅ Статья удалена из каталога {catalog.title}",
                reply_markup=get_catalog_articles_kb(catalog.id)
            )
            
    except Exception as e:
        logging.error(f"Delete article error: {e}")
        await handle_user_errors(callback)

# Просмотр публичного каталога
@user_router.callback_query(F.data.startswith("view_public_catalog_"))
async def view_public_catalog(callback: CallbackQuery):
    try:
        catalog_id = int(callback.data.split("_")[-1])
        
        async with async_session() as session:
            
            repo = CatalogRepository(session)
            catalog = await repo.get_catalog_by_id(catalog_id)
            
            if not catalog or catalog.private != PrivateEnum.PUBLIC:
                await callback.answer("❌ Каталог недоступен")
                return
            
            articles = await ArticleRepository(session).get_articles(catalog_id)
            articles_text = "\n".join(
                [f"📌 {art.description[:50]}..." for art in articles]
            )
            
            text = (
                f"📁 Публичный каталог: {hbold(catalog.title)}\n"
                f"👤 Автор: {catalog.user_id}\n"
                f"📅 Создан: {catalog.date.strftime('%d.%m.%Y')}\n\n"
                f"📚 Статьи ({len(articles)}):\n{articles_text}"
            )
            
            await callback.message.edit_text(
                text,
                parse_mode="HTML",
                reply_markup=get_public_catalog_kb(catalog_id)
            )
            
    except Exception as e:
        logging.error(f"View public catalog error: {e}")
        await handle_user_errors(callback)

@user_router.message(Command("create_catalog"))
async def start_create_catalog(message: Message, state: FSMContext):
    await message.answer("📝 Введите название каталога:")
    await state.set_state(CatalogStates.waiting_catalog_title)


@user_router.message(CatalogStates.waiting_catalog_title)
async def process_catalog_title(message: Message, state: FSMContext):
    await state.update_data(title=message.text)
    await message.answer(
        "🔒 Выберите тип доступа:", reply_markup=get_privacy_selection_kb()
    )
    await state.set_state(CatalogStates.waiting_catalog_privacy)


@user_router.callback_query(
    CatalogStates.waiting_catalog_privacy, F.data.startswith("privacy_")
)
async def process_catalog_privacy(callback: CallbackQuery, state: FSMContext):
    try:
        data = await state.get_data()
        privacy_type = callback.data.split("_")[1]

        catalog_data = CatalogCreate(
            title=data["title"], private=privacy_type, user_id=callback.from_user.id
        )

        async with async_session() as session:
            repo = CatalogRepository(session)
            catalog = await repo.create_catalog(catalog_data)

            await callback.message.answer(
                f"✅ Каталог '{catalog.title}' успешно создан!",
                reply_markup=get_catalog_actions_kb(catalog.id),
            )

    except Exception as e:
        log.error(f"Catalog creation error: {e}")
        await callback.answer("⚠️ Ошибка при создании каталога", show_alert=True)
    finally:
        await state.clear()


@user_router.message(Command("my_catalogs"))
async def list_catalogs(message: Message):
    try:
        async with async_session() as session:
            repo = CatalogRepository(session)
            catalogs = await repo.get_user_catalogs(message.from_user.id)

            if not catalogs:
                await message.answer("📂 У вас пока нет каталогов")
                return

            kb = InlineKeyboardBuilder()
            for catalog in catalogs:
                kb.button(
                    text=f"📁 {catalog.title} ({catalog.private.value})",
                    callback_data=f"view_catalog_{catalog.id}",
                )
            kb.button(text="🔙 Назад", callback_data="back_to_main")
            kb.adjust(1)

            await message.answer("📂 Ваши каталоги:", reply_markup=kb.as_markup())

    except Exception as e:
        log.error(f"Catalog list error: {e}")
        await message.answer("⚠️ Ошибка загрузки каталогов")


@user_router.callback_query(F.data.startswith("edit_catalog_"))
async def start_edit_catalog(callback: CallbackQuery, state: FSMContext):
    catalog_id = int(callback.data.split("_")[-1])
    await state.update_data(catalog_id=catalog_id)
    await callback.message.answer(
        "✏️ Введите новое название каталога:",
        reply_markup=get_back_to_catalogs_kb(catalog_id),
    )
    await state.set_state(CatalogStates.waiting_edit_title)


@user_router.message(CatalogStates.waiting_edit_title)
async def process_edit_title(message: Message, state: FSMContext):
    try:
        data = await state.get_data()
        catalog_id = data["catalog_id"]

        async with async_session() as session:
            repo = CatalogRepository(session)
            await repo.update_catalog(catalog_id, {"title": message.text})

            catalog = await repo.get_catalog_by_id(catalog_id)
            await message.answer(
                f"✅ Каталог успешно обновлен!\nНовое название: {catalog.title}",
                reply_markup=get_catalog_actions_kb(catalog_id),
            )

    except Exception as e:
        log.error(f"Edit catalog error: {e}")
        await message.answer("⚠️ Ошибка обновления каталога")
    finally:
        await state.clear()
