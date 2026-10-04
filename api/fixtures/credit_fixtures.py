import pytest

from api.classes.api_manager import ApiManager
from api.generators.amount_generator import AmountGenerator
from api.generators.model_generator import RandomModelGenerator
from api.models.create_account_response import CreateAccountResponse
from api.models.create_user_request import CreateUserCreditRequest, CreateUserRequest
from api.models.credit_submission_response import CreditSubmissionResponse
from api.models.deposit_response import DepositResponse


@pytest.fixture()
def create_credit_user(api_manager: ApiManager):
    user_credit_request = RandomModelGenerator.generate(CreateUserCreditRequest)
    api_manager.admin_steps.create_user(user_credit_request)
    return user_credit_request

@pytest.fixture()
def create_account_credit_response(api_manager: ApiManager,
                                   create_credit_user: CreateUserRequest) -> CreateAccountResponse:
    response = api_manager.user_steps.create_account(create_credit_user)
    return response

@pytest.fixture()
def create_credit_response(api_manager: ApiManager,
                           create_credit_user: CreateUserCreditRequest,
                           create_account_credit_response: CreateAccountResponse) -> CreditSubmissionResponse:
    response = api_manager.credit_steps.create_credit(user_credit=create_credit_user,
                                                      account_response=create_account_credit_response,
                                                      amount=AmountGenerator.credit())
    return response

@pytest.fixture()
def deposit_credit_account_response(api_manager: ApiManager,
                                    create_credit_user: CreateUserCreditRequest,
                                    create_account_credit_response: CreateAccountResponse,
                                    create_credit_response: CreditSubmissionResponse) -> DepositResponse:
    response = api_manager.user_steps.change_balance(user=create_credit_user,
                                                     account_id=create_account_credit_response.id,
                                                     amount=AmountGenerator.deposit())
    return response
