
from base_client import AmazonAdsBaseClient

class ProfilesClient(AmazonAdsBaseClient):
    def __init__(self):
        super().__init__(profile_id="")

    def list_profiles(self):
        return self._request("GET", "/v2/profiles")
