import pytest

from api.models.create_user_request import CreateUserRequest


@pytest.fixture()
def create_user_request(api_manager):
    user_request = CreateUserRequest(
        username="MaxC",
        password="MaxPas!w0rd",
        role="ROLE_USER"
    )
    api_manager.admin_steps.create_user(user_request)
    return user_request