import pytest
from sqlalchemy.orm import Session
from api.classes.api_manager import ApiManager
from api.db.crud.account_crud import AccountCrudDB as Account
from api.models.create_account_response import CreateAccountResponse
from api.models.create_user_request import CreateUserRequest


@pytest.mark.api
class TestAccountBalance:
    @pytest.mark.parametrize("amount", [1000.0, 7889.5])
    def test_increase_balance(self,
                              db_session: Session,
                              api_manager: ApiManager,
                              create_user_request: CreateUserRequest,
                              create_account_response: CreateAccountResponse,
                              amount: float):
        response = api_manager.user_steps.change_balance(
            user=create_user_request,
            account_id=create_account_response.id,
            amount=amount)

        assert response.balance == pytest.approx(create_account_response.balance + amount, abs=0.1)
        account_from_db = Account.get_account_by_id(db_session, create_account_response.id)
        assert account_from_db.balance == create_account_response.balance + amount, \
            f"Баланс аккаунта с id '{create_account_response.id}' в базе данных не был увеличен на {amount}."

    @pytest.mark.parametrize("amount", [999.99, -1000.0, 0.0, -0.01, 1000000.0])
    def test_increase_balance_invalid(self,
                              db_session: Session,
                              api_manager: ApiManager,
                              create_user_request: CreateUserRequest,
                              create_account_response: CreateAccountResponse,
                              amount: float):
        response = api_manager.user_steps.change_balance_invalid(
            user=create_user_request,
            account_id=create_account_response.id,
            amount=amount)

        account_from_db = Account.get_account_by_id(db_session, create_account_response.id)
        assert account_from_db.balance == pytest.approx(create_account_response.balance, abs=0.1), \
            f"Баланс аккаунта с id '{create_account_response.id}'"\
            f" в базе данных был изменен на {amount}, но не должен был быть изменен."
