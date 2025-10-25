import httpx
from .config import settings
import logging

logger = logging.getLogger(__name__)

class TrackHSClient:
    def __init__(self):
        self.base_url = settings.trackhs_api_url
        self.auth = (settings.trackhs_username, settings.trackhs_password)
    
    async def get(self, endpoint: str, params: dict = None) -> dict:
        """GET request a TrackHS API"""
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.base_url}{endpoint}",
                params=params,
                auth=self.auth,
                timeout=30.0
            )
            response.raise_for_status()
            return response.json()
    
    async def post(self, endpoint: str, json: dict) -> dict:
        """POST request a TrackHS API"""
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}{endpoint}",
                json=json,
                auth=self.auth,
                timeout=30.0
            )
            response.raise_for_status()
            return response.json()

trackhs_client = TrackHSClient()
