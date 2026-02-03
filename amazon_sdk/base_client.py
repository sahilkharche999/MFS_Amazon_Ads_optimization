
import requests
from config import AmazonAdsConfig
from exceptions import ApiRequestError, RateLimitError
from auth_client import AmazonAuthClient

class AmazonAdsBaseClient:
    def __init__(self, profile_id: str):
        self.profile_id = profile_id
        self.auth = AmazonAuthClient()
        self.access_token = self.auth.refresh_access_token()

    def _headers(self):
        return {
            "Authorization": f"Bearer {self.access_token}",
            "Amazon-Advertising-API-ClientId": AmazonAdsConfig.CLIENT_ID,
            "Amazon-Advertising-API-Scope": self.profile_id,
            "Content-Type": "application/json",
        }

    def _request(self, method: str, path: str, payload=None):
        url = f"{AmazonAdsConfig.BASE_URL}{path}"

        response = requests.request(
            method=method,
            url=url,
            headers=self._headers(),
            json=payload,
            timeout=AmazonAdsConfig.TIMEOUT,
        )

        if response.status_code == 401:
            self.access_token = self.auth.refresh_access_token()
            return self._request(method, path, payload)

        if response.status_code == 429:
            raise RateLimitError("Amazon rate limit exceeded")

        if response.status_code >= 300:
            raise ApiRequestError(response.text)

        return response.json()
