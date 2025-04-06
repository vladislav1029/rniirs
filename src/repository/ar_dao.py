from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional, List
import hashlib
from datetime import datetime

from src.repository.model import Article
from src.dto.articls import ArticleCreateSchema


class ArticleRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def _generate_guid(self, link: str) -> str:
        return hashlib.md5(link.encode()).hexdigest()

    async def get_by_guid(self, guid: str) -> Optional[Article]:
        result = await self.session.execute(select(Article).where(Article.guid == guid))
        return result.scalars().first()

    async def get_by_link(self, link: str) -> Optional[Article]:
        guid = await self._generate_guid(link)
        return await self.get_by_guid(guid)

    async def create(self, article_data: dict) -> Article:
        # Генерация GUID перед сохранением
        article_data["guid"] = await self._generate_guid(article_data["link"])

        new_article = Article(**article_data)
        self.session.add(new_article)
        await self.session.commit()
        await self.session.refresh(new_article)
        return new_article

    async def update(self, guid: str, update_data: dict) -> Optional[Article]:
        # Исключаем поля, которые нельзя обновлять
        update_data.pop("guid", None)
        update_data.pop("created_at", None)

        await self.session.execute(
            update(Article).where(Article.guid == guid).values(**update_data)
        )
        await self.session.commit()
        return await self.get_by_guid(guid)

    async def delete(self, guid: str) -> bool:
        await self.session.execute(delete(Article).where(Article.guid == guid))
        await self.session.commit()
        return True

    async def upsert_from_parser(self, parsed_data: dict) -> Article:
        # Извлекаем и валидируем данные
        article_schema = ArticleCreateSchema(**parsed_data)
        data = article_schema.model_dump()
        link = data["link"]

        # Проверяем существование записи
        existing = await self.get_by_link(link)

        if existing:
            # Обновляем существующую запись
            return await self.update(existing.guid, data)
        else:
            # Создаем новую запись
            return await self.create(data)

    async def list_articles(
        self,
        limit: int = 100,
        offset: int = 0,
        published_after: Optional[datetime] = None,
    ) -> List[Article]:
        query = select(Article).limit(limit).offset(offset)

        if published_after:
            query = query.where(Article.published >= published_after)

        result = await self.session.execute(query)
        return result.scalars().all()
