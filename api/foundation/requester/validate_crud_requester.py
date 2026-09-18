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

    def post(self, model: BaseModel) -> BaseModel:
        response = self.crud_requester.post(model)
        self.response_spec(response)
        return self.endpoint.value.response_model.model_validate(response.json())

    def delete(self, user_id: int):
        response = self.crud_requester.delete(user_id)
        self.response_spec(response)
        return self.endpoint.value.response_model.model_validate(response.json())
