import pytest

from api.classes.api_manager import ApiManager
from api.generators.model_generator import RandomModelGenerator
from api.models.create_account_response import CreateAccountResponse
from api.models.create_user_request import CreateUserCreditRequest, CreateUserRequest


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