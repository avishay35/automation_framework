import httpx
import logging
from config.settings import settings

logger = logging.getLogger(__name__)


class AuthClient:
    """API client dedicated to authentication operations."""

    def __init__(self, base_url: str = None) -> None:
        #self.base_url = base_url or str(settings.api_base_url)
        self.base_url = str(settings.api_base_url)
        #self.base_url = "https://api.realworld.show/api"

    def login_and_get_token(self, email: str, password: str) -> str:
        """Executes a POST request to /users/login and returns the JWT authorization token."""
        url = f"{self.base_url.rstrip('/')}/users/login"
        payload = {
            "user": {
                "email": email,
                "password": password
            }
        }
        print(f"DEBUG: url: {url}")
        print(f"DEBUG: email: {email} :Password {password}")

        logger.info(f"Requesting JWT token from API endpoint: {url}")
        
        with httpx.Client(timeout=10.0) as client:
            response = client.post(url, json=payload)
            response.raise_for_status()
            data = response.json()
            
            token = data["user"]["token"]
            logger.info("Successfully retrieved JWT authentication token.")
            return token
