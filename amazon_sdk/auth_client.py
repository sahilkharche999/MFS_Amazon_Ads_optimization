
import requests
from config import AmazonAdsConfig
from exceptions import AuthenticationError

class AmazonAuthClient:
    def __init__(self):
        self.access_token = None

    def refresh_access_token(self) -> str:
        payload = {
            "grant_type": "refresh_token",
            "refresh_token": AmazonAdsConfig.REFRESH_TOKEN,
            "client_id": AmazonAdsConfig.CLIENT_ID,
            "client_secret": AmazonAdsConfig.CLIENT_SECRET,
        }

        response = requests.post(
            AmazonAdsConfig.AUTH_URL,
            data=payload,
            timeout=AmazonAdsConfig.TIMEOUT,
        )

        if response.status_code != 200:
            raise AuthenticationError(response.text)

        self.access_token = response.json()["access_token"]
        return self.access_token
