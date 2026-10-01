from api.foundation.endpont import Endpoint
from api.foundation.requester.validate_crud_requester import ValidateCrudRequester
from api.models.create_account_response import CreateAccountResponse
from api.models.create_user_request import CreateUserCreditRequest
from api.models.credit_submission_request import CreditSubmissionRequest
from api.models.credit_submission_response import CreditSubmissionResponse
from api.steps.base_steps import BaseSteps
from specs.request_specs import RequestSpecs
from specs.response_specs import ResponseSpecs


class UserCreditSteps(BaseSteps):
    def create_credit(self,
                      user_credit: CreateUserCreditRequest,
                      account_response: CreateAccountResponse,
                      amount: float = 5000,
                      term_months: int = 12) -> CreditSubmissionResponse:
        credit_request_data = CreditSubmissionRequest(
            account_id=account_response.id,
            amount=amount,
            term_months=term_months
            )
        response = ValidateCrudRequester(
            request_spec=RequestSpecs.auth_headers(
                username=user_credit.username,
                password=user_credit.password),
            endpoint=Endpoint.CREDIT_REQUEST,
            response_spec=ResponseSpecs.request_created()
        ).post(credit_request_data)
        return response
