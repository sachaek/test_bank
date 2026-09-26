from api.foundation.endpont import Endpoint
from api.foundation.requester.validate_crud_requester import ValidateCrudRequester
from api.models.create_account_response import CreateAccountResponse
from api.models.create_user_request import CreateUserRequest
from api.models.deposit_request import DepositRequest
from api.models.deposit_response import DepositResponse
from api.steps.base_steps import BaseSteps
from specs.request_specs import RequestSpecs
from specs.response_specs import ResponseSpecs


class UserSteps(BaseSteps):
    def create_account(self, create_user_request: CreateUserRequest) -> CreateAccountResponse:
        response = ValidateCrudRequester(
            request_spec=RequestSpecs.auth_headers(
                username=create_user_request.username,
                password=create_user_request.password),
            endpoint=Endpoint.CREATE_ACCOUNT,
            response_spec=ResponseSpecs.request_created()
        ).post()
        return response

    def change_balance(self, user: CreateUserRequest, account_id: int, amount: float) -> DepositResponse:
        deposit_request = DepositRequest(account_id=account_id, amount=amount)
        response = ValidateCrudRequester(
            request_spec=RequestSpecs.auth_headers(
                username=user.username,
                password=user.password),
            endpoint=Endpoint.ACCOUNT_DEPOSIT,
            response_spec=ResponseSpecs.request_ok()
        ).post(deposit_request)
        return response
