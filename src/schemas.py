# schemas.py
from pydantic import BaseModel
from datetime import datetime
from src.repository.models import RoleEnum, PrivateEnum

class UserCreate(BaseModel):
    id: int
    role: RoleEnum = RoleEnum.USER

class CatalogCreate(BaseModel):
    title: str
    private: PrivateEnum = PrivateEnum.PRIVATE
    user_id: int

class ArticleCreate(BaseModel):
    title: str
    description: str
    category: str
    catalog_id: int