from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models import Article


class ArticleRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_article(self, article_id: int) -> Article | None:
        return await self.session.get(Article, article_id)

    async def get_articles(self, catalog_id: int) -> list[Article]:
        result = await self.session.execute(
            select(Article).where(Article.catalog_id == catalog_id)
        )
        return result.scalars().all()

    async def delete_article(self, article_id: int) -> None:
        article = await self.get_article(article_id)
        if article:
            await self.session.delete(article)
            await self.session.commit()