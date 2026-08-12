import httpx
from src.api.base_api_client import BaseAPIClient


class ArticleClient(BaseAPIClient):
    """Business client dedicated strictly to Article resource operations."""

    def get_articles(self, limit: int = 10, offset: int = 0) -> httpx.Response:
        """GET /articles - Fetches global feed articles."""
        return self.get("/articles", params={"limit": limit, "offset": offset})

    def create_article(self, title: str, description: str, body: str, tags: list[str] = None) -> httpx.Response:
        """POST /articles - Creates a new article."""
        payload = {
            "article": {
                "title": title,
                "description": description,
                "body": body,
                "tagList": tags or []
            }
        }
        return self.post("/articles", json=payload)

    def delete_article(self, slug: str) -> httpx.Response:
        """DELETE /articles/{slug} - Deletes an article by slug."""
        return self.delete(f"/articles/{slug}")