import pytest
from sqlalchemy.orm import Session
from api.classes.api_manager import ApiManager
from api.db.crud.account_crud import AccountCrudDB as Account
from api.models.create_account_response import CreateAccountResponse
from api.models.create_user_request import CreateUserRequest


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
        account_from_db = Account.get_account_by_id(db_session, create_account_request.id)
        assert account_from_db.balance == create_account_request.balance + amount, \
            f"Баланс аккаунта с id '{create_account_request.id}' в базе данных не был увеличен на {amount}."

    @pytest.mark.parametrize("amount", [999.99, -1000.0, 0.0, -0.01, 1000000.0])
    def test_increase_balance_invalid(self,
                              db_session: Session,
                              api_manager: ApiManager,
                              create_user_request: CreateUserRequest,
                              create_account_request: CreateAccountResponse,
                              amount: float):
        response = api_manager.user_steps.change_balance_invalid(
            user=create_user_request,
            account_id=create_account_request.id,
            amount=amount)

        assert response.status_code == 400
        account_from_db = Account.get_account_by_id(db_session, create_account_request.id)
        assert account_from_db.balance == create_account_request.balance, \
            f"Баланс аккаунта с id '{create_account_request.id}'"\
            " в базе данных был изменен на {amount}, но не должен был быть изменен."
