import pytest
from sqlalchemy.orm import Session

from api.classes.api_manager import ApiManager
from api.db.crud.account_crud import AccountCrudDB as Account
from api.db.crud.credit_crud import CreditCrudDB as Credit
from api.models.create_account_response import CreateAccountResponse
from api.models.create_user_request import CreateUserCreditRequest
from api.models.credit_submission_response import CreditSubmissionResponse
from api.models.deposit_response import DepositResponse


@pytest.mark.api
class TestCredit:
    _second_credit_error = "Only one active credit allowed per user"
    _credit_amount = 5000
    _credit_term_months = 12
    _repay_amount = 5000

    def test_credit_submission(self,
                               db_session: Session,
                               api_manager: ApiManager,
                               create_credit_user: CreateUserCreditRequest,
                               create_account_credit_response: CreateAccountResponse):
        response = api_manager.credit_steps.create_credit(user_credit=create_credit_user,
                                                          account_response=create_account_credit_response)
        account_db = Account.get_account_by_id(db_session, create_account_credit_response.id)
        expected_balance = create_account_credit_response.balance + TestCredit._credit_amount

        assert account_db.balance == pytest.approx(expected_balance, abs=0.1), (
            f"Баланс аккаунта с id {create_account_credit_response.id}"
            f"в бд не увеличился на сумму кредита {TestCredit._credit_amount}"
        )
        assert response.id == create_account_credit_response.id, \
            f"неверный id акаунта в ответе "\
            f"ожидали {create_account_credit_response.id}, пришло {response.id}"
        assert response.amount == pytest.approx(TestCredit._credit_amount, abs=0.1),\
            f"сумма кредита в ответе не та, "\
            f"ожидали {TestCredit._credit_amount}, пришло {response.amount}"
        assert response.term_months == TestCredit._credit_term_months,\
            f"неправильный срок кредита в ответе "\
            f"ожидали {TestCredit._credit_term_months}, пришло {response.term_months}"
        credit_db = Credit.get_credit_by_id(db_session, response.credit_id)
        assert credit_db is not None,             f"кредит с id {response.credit_id} не нашелся в бд"
        assert credit_db.balance == pytest.approx(-TestCredit._credit_amount, abs=0.1),         f"долг по кредиту в бд не правильный, "        f"ожидали {-TestCredit._credit_amount} а там {credit_db.balance}"

    def test_second_credit_submission(self,
                                      db_session: Session,
                                      api_manager: ApiManager,
                                      create_credit_user: CreateUserCreditRequest,
                                      create_account_credit_response: CreateAccountResponse,
                                      create_credit_response: CreditSubmissionResponse):
        response = api_manager.credit_steps.create_credit_invalid(user_credit=create_credit_user,
                                                                  account_response=create_account_credit_response,
                                                                  amount=TestCredit._credit_amount,
                                                                  term_months=TestCredit._credit_term_months)
        account_db = Account.get_account_by_id(db_session, create_account_credit_response.id)
        credits_db = Credit.get_credits_by_account_id(db_session, create_account_credit_response.id)
        expected_balance = create_account_credit_response.balance + create_credit_response.amount

        assert response.json()["error"] == TestCredit._second_credit_error,\
            f"не тот текст ошибки, ожидали {TestCredit._second_credit_error} пришло {response.text}"
        assert account_db.balance == pytest.approx(expected_balance, abs=0.1),\
            f"баланс акаунта {create_account_credit_response.id} в бд поменялся после второго кредита, "\
            f"ожидали {expected_balance} а там {account_db.balance}"
        assert len(credits_db) == 1,         f"в бд должен быть один кредит на акаунт а их {len(credits_db)}"

    def test_credit_repay(self,
                          db_session: Session,
                          api_manager: ApiManager,
                          create_credit_user: CreateUserCreditRequest,
                          create_account_credit_response: CreateAccountResponse,
                          create_credit_response: CreditSubmissionResponse,
                          deposit_credit_account_response: DepositResponse):
        response = api_manager.credit_steps.repay_credit(user=create_credit_user,
                                                         account_response=create_account_credit_response,
                                                         credit_response=create_credit_response,
                                                         amount=TestCredit._repay_amount)
        account_db = Account.get_account_by_id(db_session, create_account_credit_response.id)
        credit_db = Credit.get_credit_by_id(db_session, create_credit_response.credit_id)
        expected_account_balance = deposit_credit_account_response.balance - TestCredit._repay_amount
        expected_credit_balance = -TestCredit._credit_amount + TestCredit._repay_amount

        assert response.credit_id == create_credit_response.credit_id,            f"неверный id кредита в ответе "            f"ожидали {create_credit_response.credit_id}, пришло {response.credit_id}"
        assert response.amount_deposited == pytest.approx(TestCredit._repay_amount, abs=0.1),            f"сумма погашения в ответе не та, "            f"ожидали {TestCredit._repay_amount}, пришло {response.amount_deposited}"
        assert account_db.balance == pytest.approx(expected_account_balance, abs=0.1),            f"баланс акаунта {create_account_credit_response.id} в бд не уменьшился на сумму погашения, "            f"ожидали {expected_account_balance} а там {account_db.balance}"
        assert credit_db.balance == pytest.approx(expected_credit_balance, abs=0.1),            f"долг по кредиту {create_credit_response.credit_id} в бд не уменьшился, "            f"ожидали {expected_credit_balance} а там {credit_db.balance}"
