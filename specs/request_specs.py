import requests

from api.configs.config import Config
from api.models.login_user_requests import LoginUserRequest
from api.models.login_user_response import LoginUserResponse


class RequestSpecs:
    @staticmethod
    def base_headers():
        return {
                "Content-Type": "application/json",
                "accept": "application/json",
            }

    @staticmethod
    def unauth_headers():
        return {
            "headers": RequestSpecs.base_headers()
        }

    @staticmethod
    def auth_headers(username: str, password: str):
        request = LoginUserRequest(username=username, password=password)
        response = requests.post(
            url=f"{Config.fetch("backendUrl")}/auth/token/login",
            json=request.model_dump(),
            headers=RequestSpecs.base_headers()
        )
        if response.status_code == 200:
            response_data = LoginUserResponse.model_validate(response.json())
            token = response_data.token
            headers = RequestSpecs.base_headers()
            headers["Authorization"] = f"Bearer {token}"
            return headers
        else:
            raise Exception("Failed to login")
        