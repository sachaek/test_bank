from http import HTTPStatus

import requests

from api.models.create_user_request import CreateUserRequest
from api.models.create_user_response import CreateUserResponse
from api.requests.requester import Requester


class CreateUserRequester(Requester):
    def post(self, create_user_request: CreateUserRequest):
        url=f"{self.base_url}/admin/create"
        response = requests.post(
            url=url,
            headers=self.headers,
            json=create_user_request.model_dump()
        )
        self.response_spec(response)
        if response.status_code in (HTTPStatus.OK, HTTPStatus.CREATED):
            return CreateUserResponse.model_validate(response.json())
        else:
            return response