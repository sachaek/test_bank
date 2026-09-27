import pytest
from sqlalchemy.orm import Session

from api.classes.api_manager import ApiManager
from api.models.create_account_response import CreateAccountResponse
from api.models.create_user_request import CreateUserRequest


@pytest.mark.api
class TestAccountTransfer:
    @pytest.mark.parametrize("amount", [1000.0, 7889.5])
    def test_transfer(self,
                      db_session: Session,
                      api_manager: ApiManager,
                      create_user_request: CreateUserRequest,
                      create_account_response: CreateAccountResponse,
                      create_account_not_empty_balance_response: CreateAccountResponse,
                      amount: float):
        response = api_manager.user_steps.transfer(
            user=create_user_request,
            account=create_account_not_empty_balance_response,
            to_account=create_account_response,
            amount=amount
        )

        assert response.from_account_id == create_account_not_empty_balance_response.id
        assert response.to_account_id == create_account_response.id
        assert response.from_account_id_balance == pytest.approx(
            create_account_not_empty_balance_response.balance - amount, abs=0.1
        )