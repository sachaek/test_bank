import pytest
from sqlalchemy.orm import Session

from api.classes.api_manager import ApiManager
from api.db.crud.account_crud import AccountCrudDB as Account
from api.generators.model_generator import RandomModelGenerator
from api.models.create_account_response import CreateAccountResponse
from api.models.create_user_request import CreateUserRequest
from api.models.deposit_request import DepositRequest


@pytest.mark.api
class TestAccountBalance:
    @pytest.mark.parametrize("amount", [1000.0])
    def test_increase_balance(self,
                              db_session: Session,
                              api_manager: ApiManager,
                              create_user_request: CreateUserRequest,
                              create_account_request: CreateAccountResponse,
                              amount: float):
        response = api_manager.user_steps.change_balance(
            user=create_user_request,
            account_id=create_account_request.id,
            amount=amount)
        assert response.balance == create_account_request.balance + amount

    def increase_balance_invalid(self):