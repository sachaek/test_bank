import pytest

from api.generators.model_generator import RandomModelGenerator
from api.models.create_user_request import CreateUserRequest


@pytest.fixture()
def create_user_request(api_manager):
    user_request = RandomModelGenerator.generate(CreateUserRequest)
    api_manager.admin_steps.create_user(user_request)
    return user_request