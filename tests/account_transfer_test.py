import pytest
from sqlalchemy.orm import Session

from api.classes.api_manager import ApiManager
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

        assert from_account_db.balance == pytest.approx(
            create_account_not_empty_balance_response.balance - amount, abs=0.1
        ), (
            f"Баланс аккаунта с id '{create_account_not_empty_balance_response.id}' "
            f"в базе данных не был уменьшен на {amount}."
        )
        assert to_account_db.balance == pytest.approx(
            create_account_response.balance + amount, abs=0.1
        ), (
            f"Баланс аккаунта с id '{create_account_response.id}' "
            f"в базе данных не был увеличен на {amount}."
        )
        assert response.from_account_id == create_account_not_empty_balance_response.id,\
        f"Ответ от API содержит неверный идентификатор аккаунта отправителя. "\
        f"Ожидалось: {create_account_not_empty_balance_response.id}, получено: {response.from_account_id}."
        assert response.to_account_id == create_account_response.id, \
        f"Ответ от API содержит неверный идентификатор аккаунта получателя. "\
        f"Ожидалось: {create_account_response.id}, получено: {response.to_account_id}."
        assert response.from_account_id_balance == pytest.approx(
            create_account_not_empty_balance_response.balance - amount, abs=0.1
        ), f"Ответ от API содержит неверный баланс аккаунта отправителя. "\
        f"Ожидалось: {create_account_not_empty_balance_response.balance - amount},"\
        f" получено: {response.from_account_id_balance}."

    def test_transfer_invalid(self):