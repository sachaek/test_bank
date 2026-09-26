import pytest

from api.classes.api_manager import ApiManager
from api.generators.model_generator import RandomModelGenerator
from api.models.create_user_request import CreateUserRequest


@pytest.fixture()
def create_user_request(api_manager: ApiManager):
    user_request = RandomModelGenerator.generate(CreateUserRequest)
    api_manager.admin_steps.create_user(user_request)
    return user_request

@pytest.fixture()
def create_account_request(api_manager: ApiManager, create_user_request: CreateUserRequest):
    response = api_manager.user_steps.create_account(create_user_request)
    return response
