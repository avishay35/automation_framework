import httpx
import logging
from config.settings import settings

logger = logging.getLogger(__name__)


class BaseAPIClient:
    """Core HTTP client wrapper managing base URLs, authorization state, and headers."""

    def __init__(self, base_url: str = None, auth_token: str = None) -> None:
        self.base_url = (base_url or str(settings.api_base_url)).rstrip("/")
        self.auth_token = auth_token

    def set_token(self, token: str) -> None:
        """Sets or updates the authorization token."""
        self.auth_token = token

    def clear_token(self) -> None:
        """Clears authorization token to simulate unauthenticated requests."""
        self.auth_token = None

    def _get_headers(self) -> dict[str, str]:
        """Constructs default HTTP headers."""
        headers = {"Content-Type": "application/json"}
        if self.auth_token:
            headers["Authorization"] = f"Token {self.auth_token}"
        return headers

    def get(self, endpoint: str, params: dict = None) -> httpx.Response:
        """Executes HTTP GET request."""
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        with httpx.Client(timeout=10.0) as client:
            return client.get(url, params=params, headers=self._get_headers())

    def post(self, endpoint: str, json: dict = None) -> httpx.Response:
        """Executes HTTP POST request."""
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        with httpx.Client(timeout=10.0) as client:
            return client.post(url, json=json, headers=self._get_headers())

    def delete(self, endpoint: str) -> httpx.Response:
        """Executes HTTP DELETE request."""
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        with httpx.Client(timeout=10.0) as client:
            return client.delete(url, headers=self._get_headers())