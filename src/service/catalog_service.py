# services/catalog_service.py
from typing import Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from src.repository.catalog_repository import CatalogRepository
from src.repository.models import Catalog
from schemas import CatalogCreate

class CatalogService:
    def __init__(self, session: AsyncSession):
        self.repository = CatalogRepository(session)
        self.session = session

    async def create_catalog(self, catalog_data: CatalogCreate) -> Catalog:
        return await self.repository.create_catalog(catalog_data)

    async def get_catalog(self, catalog_id: int) -> Optional[Catalog]:
        return await self.repository.get_catalog_by_id(catalog_id)

    async def update_catalog(self, catalog_id: int, update_data: dict) -> Catalog:
        return await self.repository.update_catalog(catalog_id, update_data)

    async def delete_catalog(self, catalog_id: int) -> None:
        await self.repository.delete_catalog(catalog_id)

    async def list_user_catalogs(self, user_id: int) -> List[Catalog]:
        return await self.repository.get_user_catalogs(user_id)

    async def list_all_catalogs(self) -> List[Catalog]:
        return await self.repository.get_all_catalogs()