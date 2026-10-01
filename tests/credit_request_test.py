import pytest
from sqlalchemy.orm import Session

from api.classes.api_manager import ApiManager
from api.db.crud.account_crud import AccountCrudDB as Account
from api.models.create_account_response import CreateAccountResponse
from api.models.create_user_request import CreateUserCreditRequest


@pytest.mark.api
class TestCredit:
    _credit_amount = 5000
    _credit_term_months = 12

    def test_credit_submission(self,
                               db_session: Session,
                               api_manager: ApiManager,
                               create_credit_user: CreateUserCreditRequest,
                               create_account_credit_response: CreateAccountResponse):
        response = api_manager.credit_steps.create_credit(user_credit=create_credit_user,
                                                          account_response=create_account_credit_response,
                                                          amount=TestCredit._credit_amount,
                                                          term_months=TestCredit._credit_term_months)
        account_db = Account.get_account_by_id(db_session, create_account_credit_response.id)
        expected_balance = create_account_credit_response.balance + TestCredit._credit_amount

        assert account_db.balance == pytest.approx(expected_balance, abs=0.1), (
            f"Баланс аккаунта с id '{create_account_credit_response.id}' "
            f"в базе данных не был увеличен на сумму кредита {TestCredit._credit_amount}."
        )
        assert response.id == create_account_credit_response.id, \
        f"Ответ от API содержит неверный идентификатор аккаунта. "\
        f"Ожидалось: {create_account_credit_response.id}, получено: {response.id}."
        assert response.amount == pytest.approx(TestCredit._credit_amount, abs=0.1), \
        f"Ответ от API содержит неверную сумму кредита. "\
        f"Ожидалось: {TestCredit._credit_amount}, получено: {response.amount}."
        assert response.term_months == TestCredit._credit_term_months, \
        f"Ответ от API содержит неверный срок кредита. "\
        f"Ожидалось: {TestCredit._credit_term_months}, получено: {response.term_months}."
        assert response.balance == pytest.approx(expected_balance, abs=0.1), \
        f"Ответ от API содержит неверный баланс аккаунта. "\
        f"Ожидалось: {expected_balance}, получено: {response.balance}."
        assert response.credit_id is not None, \
        "Ответ от API не содержит идентификатор кредита."
