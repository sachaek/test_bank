from api.foundation.endpont import Endpoint
from api.foundation.requester.validate_crud_requester import ValidateCrudRequester
from api.models.create_user_request import CreateUserCreditRequest
from api.models.credit_submission_response import CreditSubmissionResponse
from api.steps.base_steps import BaseSteps
from specs.request_specs import RequestSpecs
from specs.response_specs import ResponseSpecs


class UserCreditSteps(BaseSteps):
    def create_credit(self, create_user_credit_request: CreateUserCreditRequest) -> CreditSubmissionResponse:
        response = ValidateCrudRequester(
            request_spec=RequestSpecs.auth_headers(
                username=create_user_credit_request.username,
                password=create_user_credit_request.password),
            endpoint=Endpoint.CREDIT_REQUEST,
            response_spec=ResponseSpecs.request_created()
        ).post()
        return response
