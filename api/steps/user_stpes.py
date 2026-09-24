from api.foundation.endpont import Endpoint
from api.foundation.requester.validate_crud_requester import ValidateCrudRequester
from api.models.create_user_request import CreateUserRequest
from api.steps.base_steps import BaseSteps
from specs.request_specs import RequestSpecs
from specs.response_specs import ResponseSpecs


class UserSteps(BaseSteps):
    def create_account(self, create_user_request: CreateUserRequest):
        response = ValidateCrudRequester(
            request_spec=RequestSpecs.auth_headers(
                username=create_user_request.username,
                password=create_user_request.password),
            endpoint=Endpoint.CREATE_ACCOUNT,
            response_spec=ResponseSpecs.request_created()
        ).post()
        return response

    def change_balance(self, create_user_request: CreateUserRequest):
        response = ValidateCrudRequester(
            request_spec=RequestSpecs.auth_headers(
                username=create_user_request.username,
                password=create_user_request.password),
            endpoint=Endpoint.ACCOUNT_DEPOSIT,
            response_spec=ResponseSpecs.request_ok()
        ).post()
        return response
