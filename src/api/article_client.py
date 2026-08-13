import httpx
from src.api.base_api_client import BaseAPIClient
from src.api.models.article import MultipleArticlesResponse, SingleArticleResponse


class ArticleClient(BaseAPIClient):
    """Business client dedicated strictly to Article resource operations."""

    def get_articles(self, limit: int = 10, offset: int = 0) -> httpx.Response:
        """GET /articles - Fetches global feed articles."""
        return self.get("/articles", params={"limit": limit, "offset": offset})
        
    #def get_articles(self, limit: int = 10, offset: int = 0) -> tuple[httpx.Response, MultipleArticlesResponse | None]:
    #    """GET /articles - Returns raw response and parsed Pydantic model if successful."""
    #    res = self.get("/articles", params={"limit": limit, "offset": offset})
    #    parsed = self.validate_response(res, MultipleArticlesResponse) if res.status_code == 200 else None
    #    return res, parsed    

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