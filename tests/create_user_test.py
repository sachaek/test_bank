import pytest
from api.models.create_user_request import CreateUserRequest
from api.requests.create_user_requester import CreateUserRequester
from specs.request_specs import RequestSpecs
from specs.response_specs import ResponseSpecs


@pytest.mark.api
class TestCreateUser:
    def test_create_user_valid(self, api_manager):
        create_user_request = CreateUserRequest(
            username="Max18191722",
            password="MaxPas!w0rd",
            role="ROLE_USER"
        )

        response = api_manager.admin_steps.create_user(create_user_request)

        assert create_user_request.username == response.username
        assert create_user_request.role == response.role

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
        create_user_request = CreateUserRequest(
            username=username,
            password=password,
            role="ROLE_USER"
        )
        CreateUserRequester(
            request_spec=RequestSpecs.auth_headers(username="admin", password="123456"),
            response_spec=ResponseSpecs.request_bad()
        ).post(create_user_request)