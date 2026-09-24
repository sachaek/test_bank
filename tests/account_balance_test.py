import pytest
from sqlalchemy.orm import Session

from api.classes.api_manager import ApiManager
from api.db.crud.account_crud import AccountCrudDB as Account
from api.models.create_user_request import CreateUserRequest


@pytest.mark.api
class TestAccountBalance:
    def test_increase_balance(self, db_session: Session, api_manager: ApiManager, create_user_request: CreateUserRequest):
        response = api_manager.user_steps.create_account(create_user_request)
        assert response.balance == 0

        account_from_db = Account.get_account_by_id(db=db_session, account_id=response.id)
        assert account_from_db.id == response.id, f"Аккаунт с id '{response.id}' не был создан в базе данных."
        assert account_from_db.balance is not None, f"Аккаунт с id '{response.id}' был создан, но баланс не был установлен."