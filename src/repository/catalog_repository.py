from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from src.models import Catalog
from src.schemas import CatalogCreate

class CatalogRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_catalog(self, catalog_data: CatalogCreate) -> Catalog:
        catalog = Catalog(
            title=catalog_data.title,
            private=catalog_data.private,
            user_id=catalog_data.user_id
        )
        self.session.add(catalog)
        await self.session.commit()
        await self.session.refresh(catalog)
        return catalog

    async def get_catalog_by_id(self, catalog_id: int) -> Catalog | None:
        return await self.session.get(Catalog, catalog_id)

    async def get_user_catalogs(self, user_id: int) -> list[Catalog]:
        result = await self.session.execute(
            select(Catalog).where(Catalog.user_id == user_id)
        )
        return result.scalars().all()

    async def update_catalog(self, catalog_id: int, update_data: dict) -> Catalog:
        catalog = await self.get_catalog_by_id(catalog_id)
        if not catalog:
            raise ValueError("Catalog not found")
        
        for key, value in update_data.items():
            setattr(catalog, key, value)
        
        await self.session.commit()
        await self.session.refresh(catalog)
        return catalog

    async def delete_catalog(self, catalog_id: int) -> None:
        catalog = await self.get_catalog_by_id(catalog_id)
        if not catalog:
            raise ValueError("Catalog not found")
        await self.session.delete(catalog)
        await self.session.commit()