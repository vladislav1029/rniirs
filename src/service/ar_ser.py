from datetime import datetime
from typing import List, Optional
from pydantic import ValidationError
from sqlalchemy.ext.asyncio import AsyncSession
import logging

logger = logging.getLogger(__name__)


class ArticleService:
    def __init__(self, repository):
        self.repository = repository

    async def get_article(self, guid: str) -> Optional[dict]:
        try:
            article = await self.repository.get_by_guid(guid)
            return article.to_dict() if article else None
        except Exception as e:
            logger.error(f"Error getting article {guid}: {e}")
            raise

    async def create_article(self, data: dict) -> dict:
        try:
            article = await self.repository.create(data)
            return article.model_dump()
        except ValidationError as e:
            logger.error(f"Validation error: {e}")
            raise
        except Exception as e:
            logger.error(f"Error creating article: {e}")
            raise

    async def upsert_from_parser(self, data: dict) -> dict:
        try:
            article = await self.repository.upsert_from_parser(data)
            return article.to_dict()
        except ValidationError as e:
            logger.error(f"Validation error: {e}")
            raise
        except Exception as e:
            logger.error(f"Error creating article: {e}")
            raise

    async def update_article(self, guid: str, update_data: dict) -> dict:
        try:
            existing = await self.repository.get_by_guid(guid)
            if not existing:
                raise ValueError("Article not found")

            updated = await self.repository.update(guid, update_data)
            return updated.to_dict()
        except ValidationError as e:
            logger.error(f"Validation error: {e}")
            raise
        except Exception as e:
            logger.error(f"Error updating article {guid}: {e}")
            raise

    async def delete_article(self, guid: str) -> bool:
        try:
            return await self.repository.delete(guid)
        except Exception as e:
            logger.error(f"Error deleting article {guid}: {e}")
            raise

    async def process_parsed_data(self, parsed_data: dict) -> dict:
        try:
            article = await self.repository.upsert_from_parser(parsed_data)
            return article.to_dict()
        except ValidationError as e:
            logger.error(f"Invalid parsed data: {e}")
            raise
        except Exception as e:
            logger.error(f"Error processing parsed data: {e}")
            raise

    async def list_articles(
        self,
        page: int = 1,
        per_page: int = 20,
        published_after: Optional[datetime] = None,
    ) -> dict:
        try:
            offset = (page - 1) * per_page
            articles = await self.repository.list_articles(
                limit=per_page, offset=offset, published_after=published_after
            )
            total = await self.repository.get_total_count(published_after)

            return {
                "items": [a.to_dict() for a in articles],
                "total": total,
                "page": page,
                "per_page": per_page,
            }
        except Exception as e:
            logger.error(f"Error listing articles: {e}")
            raise

    async def search_articles(self, query: str) -> List[dict]:
        try:
            articles = await self.repository.search(query)
            return [a.to_dict() for a in articles]
        except Exception as e:
            logger.error(f"Search error for '{query}': {e}")
            raise
