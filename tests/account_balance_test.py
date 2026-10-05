import pytest
from sqlalchemy.orm import Session
from api.assertions.account_assertions import AccountAssert
from api.assertions.base_assertions import BaseAssert
from api.classes.api_manager import ApiManager
from api.constants.limits import Limits
from api.db.crud.account_crud import AccountCrudDB as Account
from api.generators.amount_generator import AmountGenerator
from api.models.create_account_response import CreateAccountResponse
from api.models.create_user_request import CreateUserRequest


@pytest.mark.api
class TestAccountBalance:
    def test_increase_balance(self,
                              db_session: Session,
                              api_manager: ApiManager,
                              create_user_request: CreateUserRequest,
                              create_account_response: CreateAccountResponse):
        amount = AmountGenerator.deposit()
        response = api_manager.user_steps.change_balance(
            user=create_user_request,
            account_id=create_account_response.id,
            amount=amount)

        account_from_db = Account.get_account_by_id(db_session, create_account_response.id)

        AccountAssert.balance_increased_by(account_db=account_from_db,
                                           balance_before=create_account_response.balance,
                                           amount=amount)
        BaseAssert.float_equal(actual=response.balance,
                               expected=account_from_db.balance,
                               message=f"баланс в ответе не совпадает с бд, "
                                       f"в бд {account_from_db.balance} пришло {response.balance}")

    @pytest.mark.parametrize("amount", [
        Limits.DEPOSIT_MIN - 0.01,
        -Limits.DEPOSIT_MIN,
        0,
        -0.01,
        Limits.DEPOSIT_MAX + 0.01,
    ])
    def test_increase_balance_invalid(self,
                              db_session: Session,
                              api_manager: ApiManager,
                              create_user_request: CreateUserRequest,
                              create_account_response: CreateAccountResponse,
                              amount: float):
        api_manager.user_steps.change_balance_invalid(
            user=create_user_request,
            account_id=create_account_response.id,
            amount=amount)

        account_from_db = Account.get_account_by_id(db_session, create_account_response.id)

        AccountAssert.balance_unchanged(account_db=account_from_db,
                                        balance_before=create_account_response.balance)
