import asyncio

from sqlalchemy.ext.asyncio import AsyncSession
from src.parser_rss import get_articles_from_feed, parse_articles

from src.repository.ar_dao import ArticleRepository
from src.repository.db_helper import async_session, create_table
from src.service.ar_ser import ArticleService


import asyncio
from contextlib import asynccontextmanager
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

# Ваши импорты для моделей и сервисов
# from your_module import ArticleRepository, ArticleService, parse_articles, create_table

@asynccontextmanager
async def get_db_session():
    engine = create_async_engine("sqlite+aiosqlite:///test.db")
    async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)
    
    async with async_session() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()

async def test_all():
    url = "https://rscf.ru/news/rss/"
    limit = 1
    articles = parse_articles(url, limit)  # Убедитесь, что эта функция асинхронная если нужно
    return articles[0]

async def get_article_service(data: dict):
    async with get_db_session() as session:
        repo = ArticleRepository(session)  # Убрать await
        service = ArticleService(repo)
        result = await service.create_article(data)
        return result

async def main():
    article_data = await test_all()
    await create_table()  # Убедитесь, что эта функция асинхронная
    
    # Если article_data - Pydantic модель
    data = article_data.model_dump() if hasattr(article_data, 'model_dump') else article_data
    
    result = await get_article_service(data)
    print("Result:", result)

if __name__ == "__main__":
    asyncio.run(main())