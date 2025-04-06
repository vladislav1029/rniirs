import asyncio
from logging import getLogger
from aiogram import Bot, Dispatcher,  types
from aiogram.filters import Command
from aiogram.utils.markdown import hbold

from src.repository.db_helper import create_table
from .log_conf import setup_logging
from .config import settings


# Initialize bot and dispatcher
bot = Bot(token=settings.BOT_TOKEN)

dp = Dispatcher()

setup_logging()
log = getLogger(__name__)





async def main():
    await create_table()
    from .routers import routers as rt
    for router in rt:
        dp.include_router(router)
    await dp.start_polling(bot)


if __name__ == "__main__":
    log.info("Проект запускается")
    asyncio.run(main())
    log.warning("лонгпулл ушел погулять")
