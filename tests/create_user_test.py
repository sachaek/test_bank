import requests
import pytest

from api.models.create_user_request import CreateUserRequest
from api.models.create_user_response import CreateUserResponse
from api.models.login_user_response import LoginUserResponse
from api.models.login_user_requests import LoginUserRequest


@pytest.mark.api
class TestCreateUser:
    def test_create_user_valid(self):
        login_user_request = LoginUserRequest(
            username="admin",
            password="123456"
        )

        r_auth = requests.post(
            url="http://localhost:4111/api/auth/token/login",
            json=login_user_request.model_dump()
        )
        assert r_auth.status_code == 200
        login_user_response = LoginUserResponse.model_validate(r_auth.json())
        assert login_user_request.username == login_user_response.user.username
        assert login_user_response.user.role == "ROLE_ADMIN"

        token = login_user_response.token

        create_user_request = CreateUserRequest(
            username="alex77723331",
            password="12345Alex%",
            role="ROLE_USER",
        )

        headers_create_user = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {token}"
        }
        response = requests.post(
            url="http://localhost:4111/api/admin/create",
            json=create_user_request.model_dump(),
            headers=headers_create_user
        )

        assert response.status_code == 200
        create_user_response = CreateUserResponse(**response.json())
        assert create_user_request.username == create_user_response.username
        assert create_user_request.role == create_user_response.role

    @pytest.mark.parametrize(
        "username, password",
        [
            ("абв", "Pas!w0rd"),
            ("ab", "Pas!w0rd"),
            ("abv!", "Pas!w0rd"),
            ("Maxx1", "Pas!w0rд"),
            ("Maxx2", "Pas!w0"),
            ("Maxx3", "pas!w0rd"),
            ("Maxx4", "PAS!W0RD"),
            ("Maxx5", "PAS!WORD"),
            ("Maxx6", "PASSW0RD")
        ]
    )
    def test_create_user_invalid(self, username, password):
        login_user_request = LoginUserRequest(
            username="admin",
            password="123456"
        )

        r_auth = requests.post(
            url="http://localhost:4111/api/auth/token/login",
            json=login_user_request.model_dump()
        )
        assert r_auth.status_code == 200
        response_auth = r_auth.json()
        token = response_auth.get("token")

        create_user_request = CreateUserRequest(
            username=username,
            password=password,
            role="ROLE_USER"
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

        assert r_create_user.status_code == 400