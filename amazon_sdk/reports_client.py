
import time
import requests
import gzip
import json
from base_client import AmazonAdsBaseClient

class ReportsClient(AmazonAdsBaseClient):
    def create_report(self, payload: dict) -> str:
        response = self._request("POST", "/v2/sp/reports", payload)
        return response["reportId"]

    def wait_for_report(self, report_id: str) -> dict:
        while True:
            result = self._request("GET", f"/v2/reports/{report_id}")

            if result["status"] == "SUCCESS":
                return result

            if result["status"] == "FAILURE":
                raise Exception("Report generation failed")

            time.sleep(10)

    def download_report(self, url: str) -> dict:
        response = requests.get(url)
        content = gzip.decompress(response.content)
        return json.loads(content.decode("utf-8"))
