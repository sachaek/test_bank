import pytest

from api.constants.roles import Role
from api.models.login_user_requests import LoginUserRequest


@pytest.mark.api
class TestUserLogin:
    def test_login_admin(self, api_manager):
        login_user_request = LoginUserRequest(
            username="admin",
            password="123456"
        )
        response = api_manager.admin_steps.login_user(login_user_request)

        assert login_user_request.username == response.user.username
        assert response.user.role == Role.ADMIN

    def test_login_user(self, api_manager, create_user_request):
        login_user_request = LoginUserRequest(
            username=create_user_request.username,
            password=create_user_request.password
        )
        response = api_manager.admin_steps.login_user(login_user_request)

        assert login_user_request.username == response.user.username
        assert response.user.role == Role.USER