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
    def test_login_admin(self):
        login_user_request = LoginUserRequest(
            username="admin",
            password="123456"
        )
        response = LoginUserRequester(
            request_spec=RequestSpecs.unauth_headers(),
            response_spec=ResponseSpecs.request_ok()
        ).post(login_user_request)

        assert login_user_request.username == response.user.username
        assert response.user.role == "ROLE_ADMIN"

    def test_login_user(self):
        create_user_request = CreateUserRequest(
            username="July123845",
            password="MaxPas!w0rd",
            role="ROLE_USER"
        )

        CreateUserRequester(
            request_spec=RequestSpecs.auth_headers(username="admin", password="123456"),
            response_spec=ResponseSpecs.request_ok()
        ).post(create_user_request)

        login_user_request = LoginUserRequest(
            username="July123845",
            password="MaxPas!w0rd"
        )
        response = LoginUserRequester(
            request_spec=RequestSpecs.unauth_headers(),
            response_spec=ResponseSpecs.request_ok()
        ).post(login_user_request)

        assert login_user_request.username == response.user.username
        assert response.user.role == "ROLE_USER"