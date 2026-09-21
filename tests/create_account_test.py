import pytest

from api.models.create_user_request import CreateUserRequest
from api.requests.create_user_requester import CreateUserRequester
from specs.request_specs import RequestSpecs
from specs.response_specs import ResponseSpecs
from api.requests.create_account_requester import CreateAccountRequester


@pytest.mark.api
class TestCreateAccount:
    def test_create_account(self, api_manager, create_user_request):
        response = api_manager.user_steps.create_account(create_user_request)
        assert response.balance == 0