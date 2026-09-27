import pytest
from sqlalchemy.orm import Session

from api.classes.api_manager import ApiManager
from api.models.create_account_response import CreateAccountResponse
from api.models.create_user_request import CreateUserRequest


class AccountTransferTest:
    @pytest.mark.parametrize("amount", [1000.0, 7889.5])
    def test_transfer(self,
                      db_session: Session,
                      api_manager: ApiManager,
                      create_user_request: CreateUserRequest,
                      create_account_response: CreateAccountResponse,
                      create_account_response_2: CreateAccountResponse,
                      amount: float):
        response = api_manager.user_steps.transfer(
            user=create_user_request,
            account=create_account_response,
            to_account=create_account_response_2,
            amount=amount
        )