import requests
import pytest


@pytest.mark.api
class TestCreateAccount:
    def test_create_account(self):
        # auth admin
        body_auth = {
            "username": "admin",
            "password": "123456"
        }
        r_auth = requests.post(
            url="http://localhost:4111/api/auth/token/login",
            json=body_auth
        )
        assert r_auth.status_code == 200
        response_auth = r_auth.json()
        # получение токена
        token = response_auth.get("token")

        body_create_user = {
            "username": "alex200122",
            "password": "12345Alex%",
            "role": "ROLE_USER"
        }
        headers_create_user = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {token}"
        }
        r_create_user = requests.post(
            url="http://localhost:4111/api/admin/create",
            json=body_create_user,
            headers=headers_create_user
        )

        assert r_create_user.status_code == 200

        login_user_response = requests.post(
            url="http://localhost:4111/api/auth/token/login",
            json={
                "username": "alex200122",
                "password": "12345Alex%",
            },
            headers={
                "Content-Type": "application/json",
                "accept": "application/json",
            }
        )

        assert login_user_response.status_code == 200
        token = login_user_response.json().get("token")

        create_account_response = requests.post(
            url="http://localhost:4111/api/account/create",
            headers={
                "accept": "application/json",
                "Authorization": f"Bearer {token}"
            }
        )

        assert create_account_response.status_code == 201
        assert create_account_response.json()["balance"] == 0