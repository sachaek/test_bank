import pytest

from api.generators.model_generator import RandomModelGenerator
from api.models.create_user_request import CreateUserRequest


@pytest.mark.api
class TestCreateUser:
    @pytest.mark.parametrize(
        "create_user_request",
        [RandomModelGenerator.generate(CreateUserRequest)]
    )
    def test_create_user_valid(self, api_manager, create_user_request):
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
    def test_create_user_invalid(self, username, password, api_manager):
        create_user_request = CreateUserRequest(
            username=username,
            password=password,
            role="ROLE_USER"
        )
        api_manager.admin_steps.create_invalid_user(create_user_request)