from typing import Optional

import requests
from requests import Response
import allure

from api.configs.config import Config
from api.foundation.http_requester import HttpRequester
from api.models.base_model import BaseModel


class CrudRequester(HttpRequester):
    def post(self, model: Optional[BaseModel]) -> Response:
        body = model.model_dump() if model is not None else ""

        with allure.step(f"POST request to {self.endpoint.value.url}"):
            allure.attach(str(body), "Request Body", allure.attachment_type.JSON)

        response = requests.post(
            url=f"{Config.fetch("backendUrl")}{self.endpoint.value.url}",
            headers=self.request_spec,
            json=body
        )

        allure.attach(
            response.text,
            "Response Body",
            allure.attachment_type.JSON
        )

        self.response_spec(response)
        return response

    def delete(self, user_id: int) -> Response:
        with allure.step(f"DELETE request to {self.endpoint.value.url}/{user_id}"):
            allure.attach(f"Deleting user with ID: {user_id}", "Request Info", allure.attachment_type.TEXT)

        response = requests.delete(
            url=f"{Config.fetch("backendUrl")}{self.endpoint.value.url}/{user_id}",
            headers=self.request_spec
        )
        allure.attach(
            response.text,
            "Response Body",
            allure.attachment_type.JSON
        )
        self.response_spec(response)
        return response