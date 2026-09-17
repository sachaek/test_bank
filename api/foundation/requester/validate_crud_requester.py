from api.foundation.http_requester import HttpRequester
from api.foundation.requester.crud_requester import CrudRequester


class ValidateCrudRequester(HttpRequester):
    def __init__(self, request_spec, endpoint, response_spec):
        super().__init__(request_spec=request_spec, endpoint=endpoint, response_spec=response_spec)
        self.crud_requester = CrudRequester(
            request_spec=request_spec,
            endpoint=endpoint,
            response_spec=response_spec
        )
