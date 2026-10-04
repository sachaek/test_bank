import pytest
from sqlalchemy.orm import Session

from api.assertions.account_assertions import AccountAssert
from api.assertions.base_assertions import BaseAssert
from api.classes.api_manager import ApiManager
from api.constants.transfer_constants import TransferDefaults
from api.db.crud.account_crud import AccountCrudDB as Account
from api.models.create_account_response import CreateAccountResponse
from api.models.create_user_request import CreateUserRequest
from api.models.deposit_response import DepositResponse


@pytest.mark.api
class TestAccountTransfer:
    @pytest.mark.parametrize("amount", [1000.0, 7889.5])
    def test_transfer(self,
                      db_session: Session,
                      api_manager: ApiManager,
                      create_user_request: CreateUserRequest,
                      create_account_response: CreateAccountResponse,
                      create_account_not_empty_balance_response: DepositResponse,
                      amount: float):
        response = api_manager.user_steps.transfer(
            user=create_user_request,
            account=create_account_not_empty_balance_response,
            to_account=create_account_response,
            amount=amount
        )
        from_account_db = Account.get_account_by_id(db_session, create_account_not_empty_balance_response.id)
        to_account_db = Account.get_account_by_id(db_session, create_account_response.id)

        AccountAssert.balance_decreased_by(account_db=from_account_db,
                                           balance_before=create_account_not_empty_balance_response.balance,
                                           amount=amount)
        AccountAssert.balance_increased_by(account_db=to_account_db,
                                           balance_before=create_account_response.balance,
                                           amount=amount)
        BaseAssert.float_equal(actual=response.from_account_id_balance,
                               expected=from_account_db.balance,
                               message=f"баланс отправителя в ответе не совпадает с бд, "
                                       f"в бд {from_account_db.balance} пришло {response.from_account_id_balance}")

    def test_transfer_foreign_account(self,
                              db_session: Session,
                              api_manager: ApiManager,
                              create_user_request: CreateUserRequest,
                              create_user_request_2: CreateUserRequest,
                              create_account_response: CreateAccountResponse,
                              create_account_not_empty_balance_response: DepositResponse):
        api_manager.user_steps.transfer_foreign_user(
            user=create_user_request_2,
            account=create_account_not_empty_balance_response,
            to_account=create_account_response,
            amount=TransferDefaults.FOREIGN_ACCOUNT_AMOUNT
        )
        from_account_db = Account.get_account_by_id(db_session, create_account_not_empty_balance_response.id)
        to_account_db = Account.get_account_by_id(db_session, create_account_response.id)

        AccountAssert.balance_unchanged(account_db=from_account_db,
                                        balance_before=create_account_not_empty_balance_response.balance)
        AccountAssert.balance_unchanged(account_db=to_account_db,
                                        balance_before=create_account_response.balance)