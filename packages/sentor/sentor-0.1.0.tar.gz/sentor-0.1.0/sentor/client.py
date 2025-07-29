import requests
from .exceptions import SentorAPIError, RateLimitError, AuthenticationError

class Client:
    def __init__(self, api_key, base_url="https://ml.sentor.app/api", timeout=30):
        self.api_key = api_key
        self.base_url = base_url
        self.timeout = timeout
        self.headers = {
            "x-api-key": self.api_key,
            "Content-Type": "application/json"
        }

    def analyze(self, text, entities=None):
        url = f"{self.base_url}/ml/predict"
        payload = {
            "docs": [
                {
                    "doc_id": "1",
                    "doc": text,
                    "entities": entities or []
                }
            ]
        }
        response = requests.post(url, json=payload, headers=self.headers, timeout=self.timeout)
        if response.status_code == 200:
            return response.json()
        elif response.status_code == 429:
            raise RateLimitError(response.json())
        elif response.status_code == 401:
            raise AuthenticationError(response.json())
        else:
            raise SentorAPIError(response.json())

    def check_health(self):
        url = f"{self.base_url}/health"
        response = requests.get(url, headers=self.headers, timeout=self.timeout)
        if response.status_code == 200:
            return response.json()
        else:
            raise SentorAPIError(response.json())