import requests
import pytest


@pytest.mark.api
class TestUserLogin:
    def test_login_admin(self):
        body_auth = {
            "username": "admin",
            "password": "123456"
        }
        headers_auth = {
            "Content-Type": "application/json",
            "accept": "application/json"
        }
        r_auth = requests.post(
            url="http://localhost:4111/api/auth/token/login",
            json=body_auth,
            headers=headers_auth
        )
        assert r_auth.status_code == 200
        assert r_auth.json().get("user").get("username") == "admin"
        assert r_auth.json().get("user").get("role") == "ROLE_ADMIN"

    def test_login_user(self):
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
            "username": "alex20022",
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
                "username": "alex20022",
                "password": "12345Alex%",
            },
            headers={
                "Content-Type": "application/json",
                "accept": "application/json",
            }
        )

        assert login_user_response.status_code == 200
        assert login_user_response.json().get("user").get("username") == "alex20022"
        assert login_user_response.json().get("user").get("role") == "ROLE_USER"