import allure
from requests import Response

from api.constants.credit_constants import CreditDefaults
from api.foundation.endpont import Endpoint
from api.foundation.requester.crud_requester import CrudRequester
from api.foundation.requester.validate_crud_requester import ValidateCrudRequester
from api.models.create_account_response import CreateAccountResponse
from api.models.create_user_request import CreateUserCreditRequest
from api.models.credit_repay_request import CreditRepayRequest
from api.models.credit_repay_response import CreditRepayResponse
from api.models.credit_submission_request import CreditSubmissionRequest
from api.models.credit_submission_response import CreditSubmissionResponse
from api.steps.base_steps import BaseSteps
from specs.request_specs import RequestSpecs
from specs.response_specs import ResponseSpecs


class UserCreditSteps(BaseSteps):
    @allure.step("Запрос кредита на сумму {amount} на {term_months} мес.")
    def create_credit(self,
                      user_credit: CreateUserCreditRequest,
                      account_response: CreateAccountResponse,
                      amount: float = CreditDefaults.AMOUNT,
                      term_months: int = CreditDefaults.TERM_MONTHS) -> CreditSubmissionResponse:
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

    @allure.step("Невалидный запрос кредита на сумму {amount} на {term_months} мес.")
    def create_credit_invalid(self,
                              user_credit: CreateUserCreditRequest,
                              account_response: CreateAccountResponse,
                              amount: float = CreditDefaults.AMOUNT,
                              term_months: int = CreditDefaults.TERM_MONTHS) -> Response:
        credit_request_data = CreditSubmissionRequest(
            account_id=account_response.id,
            amount=amount,
            term_months=term_months
        )
        response = CrudRequester(
            request_spec=RequestSpecs.auth_headers(
                username=user_credit.username,
                password=user_credit.password),
            endpoint=Endpoint.CREDIT_REQUEST,
            response_spec=ResponseSpecs.not_found()
        ).post(credit_request_data)
        return response

    @allure.step("Погашение кредита на сумму {amount}")
    def repay_credit(self,
                      user: CreateUserCreditRequest,
                      account_response: CreateAccountResponse,
                      credit_response: CreditSubmissionResponse,
                      amount: int = CreditDefaults.REPAY_AMOUNT) -> CreditRepayResponse:
        credit_request_data = CreditRepayRequest(
            creditId=credit_response.credit_id,
            accountId=account_response.id,
            amount=amount
        )
        response = ValidateCrudRequester(
            request_spec=RequestSpecs.auth_headers(
                username=user.username,
                password=user.password),
            endpoint=Endpoint.CREDIT_REPAY,
            response_spec=ResponseSpecs.request_ok()
        ).post(credit_request_data)
        return response

    @allure.step("Невалидное погашение кредита {credit_id} на сумму {amount} со счёта {account_id}")
    def repay_credit_invalid(self,
                             user: CreateUserCreditRequest,
                             account_id: int,
                             credit_id: int,
                             amount: int = CreditDefaults.REPAY_AMOUNT,
                             response_spec=ResponseSpecs.unprocessable_entity()) -> Response:
        credit_request_data = CreditRepayRequest(
            creditId=credit_id,
            accountId=account_id,
            amount=amount
        )
        response = CrudRequester(
            request_spec=RequestSpecs.auth_headers(
                username=user.username,
                password=user.password),
            endpoint=Endpoint.CREDIT_REPAY,
            response_spec=response_spec
        ).post(credit_request_data)
        return response
