from datetime import datetime
from pydantic import BaseModel, computed_field, field_validator, ConfigDict
from typing import List, Optional
import hashlib


class ArticleCreateSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    # Основные поля
    link: str
    title: Optional[str] = None
    summary: Optional[str] = None
    author: Optional[str] = None
    categories: List[str] = []
    image: Optional[str] = None
    published: Optional[datetime] = None
    created_at: datetime = datetime.now()
    updated_at: datetime = datetime.now()

    # Вычисляемые поля
    @computed_field
    @property
    def guid(self) -> str:
        return hashlib.md5(self.link.encode()).hexdigest()

    # Валидаторы
    @field_validator("categories", mode="before")
    @classmethod
    def extract_categories(cls, tags: list) -> List[str]:
        return [tag["term"] for tag in tags if "term" in tag]

    @field_validator("image", mode="before")
    @classmethod
    def extract_image(cls, links: list) -> Optional[str]:
        for link in links:
            if link.get("rel") == "enclosure" and "image" in link.get("type", ""):
                return link.get("href")
        return None

    @field_validator("published", mode="before")
    @classmethod
    def parse_published(cls, value: str) -> datetime:
        return datetime.strptime(value, "%a, %d %b %Y %H:%M:%S %z").replace(tzinfo=None)

    # Схема для чтения из БД (БД → клиент)


class ArticleResponseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    guid: str
    link: str
    title: Optional[str] = None
    summary: Optional[str] = None
    author: Optional[str] = None
    categories: List[str] = []
    image: Optional[str] = None
    published: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime
