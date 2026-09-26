import pytest
from sqlalchemy.orm import Session

from api.classes.api_manager import ApiManager
from api.db.crud.account_crud import AccountCrudDB as Account
from api.models.create_user_request import CreateUserRequest


@pytest.mark.api
class TestAccountBalance:
    def test_increase_balance(self,
                              db_session: Session,
                              api_manager: ApiManager,
                              create_user_request: CreateUserRequest,
                              create_account_request: CreateUserRequest):
        response = api_manager.user_steps.change_balance(user=create_user_request, account_id=create_account_request.id, amount=1000.0)
        assert response.amount == 1000.0