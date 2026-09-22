from typing import Optional
import allure

from api.configs.config import Config
from api.foundation.http_requester import HttpRequester
from api.foundation.requester.crud_requester import CrudRequester
from api.models.base_model import BaseModel


class ValidateCrudRequester(HttpRequester):
    def __init__(self, request_spec, endpoint, response_spec):
        super().__init__(request_spec=request_spec, endpoint=endpoint, response_spec=response_spec)
        self.crud_requester = CrudRequester(
            request_spec=request_spec,
            endpoint=endpoint,
            response_spec=response_spec
        )

    def post(self, model: Optional[BaseModel] | None = None) -> BaseModel:
        response = self.crud_requester.post(model)
        with allure.step(f"POST {Config.fetch('backendUrl')}{self.endpoint.value.url} and validated Model"):
            allure.attach(f"Validated Model: {self.endpoint.value.response_model.__name__}")

        self.response_spec(response)
        return self.endpoint.value.response_model.model_validate(response.json())

    def delete(self, user_id: int):
        response = self.crud_requester.delete(user_id)
        with allure.step(f"DELETE {Config.fetch('backendUrl')}{self.endpoint.value.url}/{user_id} and validated Model"):
            allure.attach(f"Validated Model: {self.endpoint.value.response_model.__name__}")

        self.response_spec(response)
        return self.endpoint.value.response_model.model_validate(response.json())
