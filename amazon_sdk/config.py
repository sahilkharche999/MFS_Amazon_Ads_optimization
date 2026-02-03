
import os

class AmazonAdsConfig:
    CLIENT_ID = os.getenv("AMAZON_CLIENT_ID")
    CLIENT_SECRET = os.getenv("AMAZON_CLIENT_SECRET")
    REFRESH_TOKEN = os.getenv("AMAZON_REFRESH_TOKEN")

    BASE_URL = "https://advertising-api.amazon.com"
    AUTH_URL = "https://api.amazon.com/auth/o2/token"

    TIMEOUT = 30
    MAX_RETRIES = 3
