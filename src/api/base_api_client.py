import httpx
import logging
from typing import Type, TypeVar
from pydantic import BaseModel, ValidationError
from config.settings import settings

logger = logging.getLogger(__name__)

T = TypeVar("T", bound=BaseModel)

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
        
    def validate_response(self, response: httpx.Response, model_cls: Type[T]) -> T:
        """Parses and validates HTTP response JSON against a Pydantic model with rich debugging context."""
        payload = response.json()
        try:
            return model_cls(**payload)
        except ValidationError as err:
            logger.error(
                f"\n❌ [CONTRACT VIOLATION] {model_cls.__name__}\n"
                f"URL: {response.request.url}\n"
                f"Received Payload Sample: {str(payload)[:300]}...\n"
                f"Validation Errors:\n{err}"
            )
            raise AssertionError(f"API Contract Violation on {model_cls.__name__}: {err}") from err    

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