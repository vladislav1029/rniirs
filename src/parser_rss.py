import aiohttp
import feedparser
from typing import List, Optional
from dataclasses import dataclass


# Сделал Паша сильно не ругать
@dataclass(frozen=True)
class Article:
    """Контейнер для данных статьи"""

    title: Optional[str]
    link: Optional[str]
    published: Optional[str]
    summary: Optional[str]
    author: Optional[str]
    categories: Optional[str]
    image: Optional[str]
    guid: Optional[str]


async def fetch_rss_content(url: str) -> str:
    """Загрузка содержимого RSS-ленты"""
    try:
        async with aiohttp.ClientSession(
            timeout=aiohttp.ClientTimeout(total=10)
        ) as session:
            async with session.get(url) as response:
                response.raise_for_status()
                return await response.text()
    except Exception as e:
        print(f"Ошибка при загрузке {url}: {e}")
        return ""


def parse_articles(content: str, limit: Optional[int] = None) -> List[Article]:
    """Разбор RSS-контента в список статей"""
    feed = feedparser.parse(content)
    if not hasattr(feed, "entries"):
        return []

    entries = feed.entries[:limit] if limit is not None else feed.entries

    articles = []
    for entry in entries:
        try:
            # Обработка изображений
            image = None
            if hasattr(entry, "media_thumbnail"):
                image = entry.media_thumbnail[0]["url"]
            elif hasattr(entry, "enclosure"):
                image = entry.enclosure.url

            # Обработка категорий
            categories = None
            if hasattr(entry, "tags"):
                categories = ", ".join(tag["term"] for tag in entry.tags)
            else:
                categories = entry.get("category")

            articles.append(
                Article(
                    title=entry.get("title"),
                    link=entry.get("link"),
                    published=entry.get("published") or entry.get("pubDate"),
                    summary=entry.get("summary") or entry.get("description"),
                    author=entry.get("author") or entry.get("creator"),
                    categories=categories,
                    image=image,
                    guid=entry.get("guid"),
                )
            )
        except Exception as e:
            print(f"Ошибка обработки статьи: {e}")

    return articles


async def get_articles_from_feed(
    url: str, limit: Optional[int] = None
) -> List[Article]:
    """
    Получение статей из RSS-ленты
    :param url: Ссылка на RSS-ленту
    :param limit: Максимальное количество статей
    :return: Список статей
    """
    content = await fetch_rss_content(url)
    if not content:
        return []

    return parse_articles(content, limit)


def display_articles_info(articles: List[Article]):
    """Вывод информации о статьях"""
    if not articles:
        print("Статьи не найдены")
        return

    print(f"\nНайдено статей: {len(articles)}")
    for i, article in enumerate(articles, 1):
        print(f"\nСтатья {i}:")
        print(f"Заголовок: {article.title or 'Нет данных'}")
        print(f"Ссылка: {article.link or 'Нет данных'}")
        print(f"Дата: {article.published or 'Нет данных'}")
        print(f"Автор: {article.author or 'Нет данных'}")
        print(f"Категории: {article.categories or 'Нет данных'}")
        print(f"Изображение: {article.image or 'Нет данных'}")
