from typing import Dict, Callable
from api.foundation.endpont import Endpoint


class HttpRequester:
    def __init__(self, request_spec: str, endpoint: Endpoint, response_spec: Callable):
        self.request_spec = request_spec
        self.endpoint = endpoint
        self.response_spec = response_spec
