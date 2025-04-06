from datetime import datetime
from typing import List, Optional


from sqlalchemy import JSON, DateTime, func
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    declared_attr,
    mapped_column,
    relationship,
)


class Base(DeclarativeBase):
    @declared_attr
    def __tablename__(cls):
        return f"{cls.__name__.lower()}s"


class Article(Base):
    __tablename__ = "articles"

    # Changed: guid is now primary key instead of id
    guid: Mapped[str] = mapped_column(primary_key=True, nullable=False)

    title: Mapped[str] = mapped_column(index=True, nullable=True)
    link: Mapped[str] = mapped_column(nullable=True)

    summary: Mapped[str] = mapped_column(nullable=True)
    author: Mapped[str] = mapped_column(nullable=True)
    categories: Mapped[List[str]] = mapped_column(JSON, nullable=True)
    image: Mapped[str] = mapped_column(nullable=True)
    published = mapped_column(DateTime, nullable=True)
    created_at = mapped_column(DateTime, default=func.now())
    updated_at = mapped_column(DateTime, default=func.now(), onupdate=func.now())
