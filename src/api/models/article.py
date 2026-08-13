from pydantic import BaseModel, Field
from datetime import datetime


class AuthorModel(BaseModel):
    username: str
    bio: str | None = None
    image: str | None = None  # Allows null/None for users without profile images
    following: bool


class ArticleModel(BaseModel):
    slug: str
    title: str
    description: str
    body: str | None = None  # Optional on feed list responses
    tagList: list[str]
    createdAt: str
    updatedAt: str
    favorited: bool
    favoritesCount: int
    author: AuthorModel


class SingleArticleResponse(BaseModel):
    article: ArticleModel


class MultipleArticlesResponse(BaseModel):
    articles: list[ArticleModel]
    articlesCount: int