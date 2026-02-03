
class AmazonAdsException(Exception):
    pass

class AuthenticationError(AmazonAdsException):
    pass

class RateLimitError(AmazonAdsException):
    pass

class ApiRequestError(AmazonAdsException):
    pass
