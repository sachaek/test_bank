import pytest
from sqlalchemy.orm import Session

from api.classes.api_manager import ApiManager
from api.generators.model_generator import RandomModelGenerator
from api.models.create_user_request import CreateUserRequest
from api.db.crud.user_crud import UserCrudDB as User


@pytest.mark.api
class TestCreateUser:
    @pytest.mark.parametrize(
        "create_user_request",
        [RandomModelGenerator.generate(CreateUserRequest)]
    )
    def test_create_user_valid(self, api_manager: ApiManager, create_user_request: CreateUserRequest, db_session: Session):
        response = api_manager.admin_steps.create_user(create_user_request)

        assert create_user_request.username == response.username
        assert create_user_request.role == response.role
        user_from_db = User.get_user_by_username(db_session, create_user_request.username)
        assert user_from_db.username == create_user_request.username,\
            f"Пользователь с username '{create_user_request.username}' не был создан в базе данных."

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
    def test_create_user_invalid(self, username: str, password: str, api_manager: ApiManager, db_session: Session):
        create_user_request = CreateUserRequest(
            username=username,
            password=password,
            role="ROLE_USER"
        )
        api_manager.admin_steps.create_invalid_user(create_user_request)

        user_from_db = User.get_user_by_username(db_session, username)
        assert user_from_db is None, f"Пользователь с username '{username}' был создан, но не должен был быть создан."