class SentorAPIError(Exception):
    def __init__(self, response):
        self.message = response.get("detail", "An error occurred")
        self.code = response.get("status_code", "unknown")
        super().__init__(self.message)

class RateLimitError(SentorAPIError):
    def __init__(self, response):
        super().__init__(response)
        self.retry_after = response.get("retry_after", 60)

class AuthenticationError(SentorAPIError):
    pass