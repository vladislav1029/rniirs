import asyncio
from logging import getLogger
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.utils.markdown import hbold


from src.parser_rss import get_articles_from_feed
from src.repository.db_helper import create_table
from .log_conf import setup_logging
from .config import settings


# Initialize bot and dispatcher
bot = Bot(token=settings.BOT_TOKEN)

dp = Dispatcher()

setup_logging()
log = getLogger(__name__)


@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer(f"Hello, {hbold(message.from_user.full_name)}!")


@dp.message()
async def echo(message: types.Message):
    await message.answer(message.text)


async def main():
    log.info("Проект запускается")
    await create_table()
    await dp.start_polling(bot)
    log.warning("лонгпулл ушел погулять")


if __name__ == "__main__":
    asyncio.run(main())
