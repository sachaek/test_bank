from http import HTTPStatus
import requests
from requests import Response

from api.models.create_account_response import CreateAccountResponse
from api.requests.requester import Requester


class CreateAccountRequester(Requester):
    def post(self, model=None) -> CreateAccountResponse | Response:
        url = f"{self.base_url}/account/create"
        response = requests.post(
            url=url,
            headers=self.headers,
        )
        self.response_spec(response)
        if response.status_code in (HTTPStatus.OK, HTTPStatus.CREATED):
            return CreateAccountResponse.model_validate(response.json())
        else:
            return response
