
from base_client import AmazonAdsBaseClient

class EntitiesClient(AmazonAdsBaseClient):
    def get_campaigns(self):
        return self._request("GET", "/v2/campaigns")

    def get_ad_groups(self):
        return self._request("GET", "/v2/adGroups")

    def get_keywords(self):
        return self._request("GET", "/v2/keywords")

    def get_product_targets(self):
        return self._request("GET", "/v2/productTargets")
