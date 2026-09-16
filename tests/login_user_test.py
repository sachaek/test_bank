import requests
import pytest

from api.models.create_user_request import CreateUserRequest
from api.models.login_user_requests import LoginUserRequest
from api.models.login_user_response import LoginUserResponse
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
            request_spec=RequestSpecs.base_headers(),
            response_spec=ResponseSpecs.request_ok()
        ).post(login_user_request)

        assert login_user_request.username == response.user.username
        assert response.user.role == "ROLE_ADMIN"

    def test_login_user(self):
        create_user_request = CreateUserRequest(
            username="Lesha3",
            password="12345Alex%",
            role="ROLE_USER",
        )
        r_create_user = requests.post(
            url="http://localhost:4111/api/admin/create",
            json=create_user_request.model_dump(),
            headers=headers_create_user
        )
        assert r_create_user.status_code == 200

        login_user_request = LoginUserRequest(
            username="Lesha3",
            password="12345Alex%",
        )

        login_user_response = requests.post(
            url="http://localhost:4111/api/auth/token/login",
            json=login_user_request.model_dump(),
            headers={
                "Content-Type": "application/json",
                "accept": "application/json",
            }
        )

        assert login_user_response.status_code == 200
        login_user_response = LoginUserResponse.model_validate(login_user_response.json())
        assert login_user_request.username == login_user_response.user.username
        assert login_user_response.user.role == "ROLE_USER"