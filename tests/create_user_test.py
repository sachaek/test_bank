import requests
import pytest


@pytest.mark.api
class TestCreateUser:
    def test_create_user_valid(self):
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
        token = response_auth.get("token")

        body_create_user = {
            "username": "alex333",
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
        assert r_create_user.json().get("username") == "alex333"
        assert r_create_user.json().get("role") == "ROLE_USER"

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
        token = response_auth.get("token")

        body_create_user = {
            "username": username,
            "password": password,
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

        assert r_create_user.status_code == 400