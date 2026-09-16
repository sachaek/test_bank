import requests
import pytest

from api.models.create_account_response import CreateAccountResponse
from api.models.create_user_request import CreateUserRequest
from api.models.login_user_requests import LoginUserRequest
from api.models.login_user_response import LoginUserResponse


@pytest.mark.api
class TestCreateAccount:
    def test_create_account(self):
        login_user_request = LoginUserRequest(
            username="admin",
            password="123456"
        )
        response = requests.post(
            url="http://localhost:4111/api/auth/token/login",
            json=login_user_request.model_dump()
        )
        assert response.status_code == 200
        login_user_response = LoginUserResponse.model_validate(response.json())
        assert login_user_request.username == login_user_response.user.username
        assert login_user_response.user.role == "ROLE_ADMIN"
        token = login_user_response.token

        create_user_request = CreateUserRequest(
            username="Lesha6",
            password="12345Alex%",
            role="ROLE_USER",
        )
        headers_create_user = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {token}"
        }
        r_create_user = requests.post(
            url="http://localhost:4111/api/admin/create",
            json=create_user_request.model_dump(),
            headers=headers_create_user
        )
        assert r_create_user.status_code == 200

        login_user_request = LoginUserRequest(
            username="Lesha6",
            password="12345Alex%",
        )
        response = requests.post(
            url="http://localhost:4111/api/auth/token/login",
            json=login_user_request.model_dump(),
            headers={
                "Content-Type": "application/json",
                "accept": "application/json",
            }
        )

        assert response.status_code == 200
        login_user_response = LoginUserResponse.model_validate(response.json())
        assert login_user_request.username == login_user_response.user.username
        assert login_user_response.user.role == "ROLE_USER"
        token = login_user_response.token

        response = requests.post(
            url="http://localhost:4111/api/account/create",
            headers={
                "accept": "application/json",
                "Authorization": f"Bearer {token}"
            }
        )
        assert response.status_code == 201
        create_account_response = CreateAccountResponse.model_validate(response.json())
        assert create_account_response.balance == 0