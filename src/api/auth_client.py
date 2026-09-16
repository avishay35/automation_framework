import httpx
import sys
import logging
from config.settings import settings

logger = logging.getLogger(__name__)


class AuthClient:
    """API client dedicated to authentication operations."""

    def __init__(self, base_url: str = None) -> None:
        self.base_url = base_url or str(settings.api_base_url)

    def login_and_get_token(self, email: str, password: str) -> str:
        """Executes a POST request to /users/login and returns the JWT authorization token."""
        url = f"{self.base_url.rstrip('/')}/users/login"
        payload = {
            "user": {
                "email": email,
                "password": password
            }
        }

        logger.info(f"Requesting JWT token from API endpoint: {url}")

        print("DEBUG: Before POST", file=sys.stderr)

        try:
            with httpx.Client(timeout=30.0) as client:
                response = client.post(url, json=payload)
        except Exception as e:
            print("DEBUG: POST exception:", e, file=sys.stderr)
            raise

        print("DEBUG: After POST", file=sys.stderr)
        print("DEBUG: Status:", response.status_code, file=sys.stderr)
        print("DEBUG: Body:", response.text, file=sys.stderr)
        
        #with httpx.Client(timeout=10.0) as client:
        #    response = client.post(url, json=payload)
        response.raise_for_status()
        data = response.json()
            
        token = data["user"]["token"]
        logger.info("Successfully retrieved JWT authentication token.")
         print("DEBUG: token:", token, file=sys.stderr)
        return token
