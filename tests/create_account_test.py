import pytest

from api.models.create_user_request import CreateUserRequest
from api.requests.create_user_requester import CreateUserRequester
from specs.request_specs import RequestSpecs
from specs.response_specs import ResponseSpecs
from api.requests.create_account_requester import CreateAccountRequester


@pytest.mark.api
class TestCreateAccount:
    def test_create_account(self):
        create_user_request = CreateUserRequest(
            username="Max55275",
            password="MaxPas!w0rd",
            role="ROLE_USER"
        )

        CreateUserRequester(
            request_spec=RequestSpecs.auth_headers(username="admin", password="123456"),
            response_spec=ResponseSpecs.request_ok()
        ).post(create_user_request)

        response = CreateAccountRequester(
            request_spec=RequestSpecs.auth_headers(username=create_user_request.username,
                                                   password=create_user_request.password),
            response_spec=ResponseSpecs.request_created()
        ).post()

        assert response.balance == 0