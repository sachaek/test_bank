import pytest

from api.classes.api_manager import ApiManager
from api.generators.model_generator import RandomModelGenerator
from api.models.create_account_response import CreateAccountResponse
from api.models.create_user_request import CreateUserRequest, CreateUserCreditRequest


@pytest.fixture()
def create_user_request(api_manager: ApiManager):
    user_request = RandomModelGenerator.generate(CreateUserRequest)
    api_manager.admin_steps.create_user(user_request)
    return user_request

@pytest.fixture()
def create_user_request_2(api_manager: ApiManager):
    user_request = RandomModelGenerator.generate(CreateUserRequest)
    api_manager.admin_steps.create_user(user_request)
    return user_request

@pytest.fixture(scope="function")
def create_account_response(api_manager: ApiManager, create_user_request: CreateUserRequest):
    response = api_manager.user_steps.create_account(create_user_request)
    return response

@pytest.fixture(scope="function")
def create_account_not_empty_balance_response(
    api_manager: ApiManager,
    create_user_request: CreateUserRequest,
    create_account_response: CreateAccountResponse,
):
    """Возвращает аккаунт с ненулевым балансом, создавая новый аккаунт и увеличивая его баланс на 9000."""
    not_empty_response = api_manager.user_steps.create_account(create_user_request)
    response = api_manager.user_steps.change_balance(
        user=create_user_request,
        account_id=not_empty_response.id,
        amount=9_000
    )
    assert response.id != create_account_response.id,\
        f"Аккаунт с id '{response.id}' был создан, но должен был быть уникальным и отличаться от id '{create_account_response.id}'."
    return response