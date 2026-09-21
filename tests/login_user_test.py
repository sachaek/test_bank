import requests
import pytest

from api.models.create_user_request import CreateUserRequest
from api.models.login_user_requests import LoginUserRequest
from api.models.login_user_response import LoginUserResponse
from api.requests.create_user_requester import CreateUserRequester
from api.requests.login_user_requester import LoginUserRequester
from specs.request_specs import RequestSpecs
from specs.response_specs import ResponseSpecs


@pytest.mark.api
class TestUserLogin:
    def test_login_admin(self, api_manager):
        login_user_request = LoginUserRequest(
            username="admin",
            password="123456"
        )
        response = api_manager.admin_steps.login_user(login_user_request)

        assert login_user_request.username == response.user.username
        assert response.user.role == "ROLE_ADMIN"

    def test_login_user(self, api_manager, create_user_request):
        login_user_request = LoginUserRequest(
            username=create_user_request.username,
            password=create_user_request.password
        )
        response = api_manager.admin_steps.login_user(login_user_request)

        assert login_user_request.username == response.user.username
        assert response.user.role == "ROLE_USER"