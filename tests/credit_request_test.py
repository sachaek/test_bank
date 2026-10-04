import pytest
from sqlalchemy.orm import Session

from api.assertions.base_assertions import BaseAssert
from api.classes.api_manager import ApiManager
from api.db.crud.account_crud import AccountCrudDB as Account
from api.db.crud.credit_crud import CreditCrudDB as Credit
from api.models.create_account_response import CreateAccountResponse
from api.models.create_user_request import CreateUserCreditRequest
from api.models.credit_submission_response import CreditSubmissionResponse
from api.models.deposit_response import DepositResponse
from api.assertions.account_assertions import AccountAssert
from api.constants.api_errors import ApiError
from api.constants.credit_constants import CreditDefaults


@pytest.mark.api
class TestCredit:
    def test_credit_submission(self,
                               db_session: Session,
                               api_manager: ApiManager,
                               create_credit_user: CreateUserCreditRequest,
                               create_account_credit_response: CreateAccountResponse):
        response = api_manager.credit_steps.create_credit(user_credit=create_credit_user,
                                                          account_response=create_account_credit_response,
                                                          amount=CreditDefaults.AMOUNT,
                                                          term_months=CreditDefaults.TERM_MONTHS)
        account_db = Account.get_account_by_id(db_session, create_account_credit_response.id)
        credit_db = Credit.get_credit_by_id(db_session, response.credit_id)
        expected_balance = create_account_credit_response.balance + CreditDefaults.AMOUNT

        AccountAssert.assert_balance_in_db(account_id=create_account_credit_response.id,
                                           account_db=account_db,
                                           expected_balance=expected_balance)
        BaseAssert.float_equal(actual=response.amount,
                               expected=CreditDefaults.AMOUNT,
                               message=f"сумма кредита в ответе некорректная, "
                                       f"ждали {CreditDefaults.AMOUNT} пришла {response.amount}")
        BaseAssert.float_equal(actual=credit_db.balance,
                               expected=pytest.approx(-CreditDefaults.AMOUNT, abs=0.1),
                               message=f"долг по кредиту в бд некорректный, "
                                       f"ждали {-CreditDefaults.AMOUNT} а там {credit_db.balance}")

    def test_second_credit_submission(self,
                                      db_session: Session,
                                      api_manager: ApiManager,
                                      create_credit_user: CreateUserCreditRequest,
                                      create_account_credit_response: CreateAccountResponse,
                                      create_credit_response: CreditSubmissionResponse):
        response = api_manager.credit_steps.create_credit_invalid(user_credit=create_credit_user,
                                                                  account_response=create_account_credit_response,
                                                                  amount=CreditDefaults.AMOUNT,
                                                                  term_months=CreditDefaults.TERM_MONTHS)
        account_db = Account.get_account_by_id(db_session, create_account_credit_response.id)
        credits_db = Credit.get_credits_by_account_id(db_session, create_account_credit_response.id)
        expected_balance = create_account_credit_response.balance + create_credit_response.amount

        assert response.json()["error"] == ApiError.ONE_ACTIVE_CREDIT, \
            f"бек вернул не ту ошибку: {response.text}"
        assert account_db.balance == pytest.approx(expected_balance, abs=0.1), \
            f"баланс аккаунта {create_account_credit_response.id} поменялся после второго кредита, ждали {expected_balance} а там {account_db.balance}"
        assert len(credits_db) == 1, f"на аккаунте должен быть 1 кредит а их {len(credits_db)}"

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
                                                         amount=CreditDefaults.REPAY_AMOUNT)
        account_db = Account.get_account_by_id(db_session, create_account_credit_response.id)
        credit_db = Credit.get_credit_by_id(db_session, create_credit_response.credit_id)
        expected_account_balance = deposit_credit_account_response.balance - CreditDefaults.REPAY_AMOUNT
        expected_credit_balance = -CreditDefaults.AMOUNT + CreditDefaults.REPAY_AMOUNT

        assert response.credit_id == create_credit_response.credit_id, \
            f"в ответе не тот id кредита, ждали {create_credit_response.credit_id} пришел {response.credit_id}"
        assert response.amount_deposited == pytest.approx(CreditDefaults.REPAY_AMOUNT, abs=0.1), \
            f"сумма погашения в ответе некорректная, ждали {CreditDefaults.REPAY_AMOUNT} пришла {response.amount_deposited}"
        assert account_db.balance == pytest.approx(expected_account_balance, abs=0.1), \
            f"с аккаунта {create_account_credit_response.id} не списались деньги, ждали {expected_account_balance} а там {account_db.balance}"
        assert credit_db.balance == pytest.approx(expected_credit_balance, abs=0.1), \
            f"долг по кредиту {create_credit_response.credit_id} не уменьшился, ждали {expected_credit_balance} а там {credit_db.balance}"

    def test_repay_more_than_debt(self,
                                  db_session: Session,
                                  api_manager: ApiManager,
                                  create_credit_user: CreateUserCreditRequest,
                                  create_credit_response: CreditSubmissionResponse,
                                  deposit_credit_account_response: DepositResponse):
        repay_amount = CreditDefaults.AMOUNT + 1000
        response = api_manager.credit_steps.repay_credit_invalid(user=create_credit_user,
                                                                 account_id=deposit_credit_account_response.id,
                                                                 credit_id=create_credit_response.credit_id,
                                                                 amount=repay_amount)
        account_db = Account.get_account_by_id(db_session, deposit_credit_account_response.id)
        credit_db = Credit.get_credit_by_id(db_session, create_credit_response.credit_id)

        assert response.json()["error"] == ApiError.REPAY_EXCEEDS_DEBT, \
            f"бек вернул не ту ошибку: {response.text}"
        assert account_db.balance == pytest.approx(deposit_credit_account_response.balance, abs=0.1), \
            f"с аккаунта {deposit_credit_account_response.id} списались деньги хотя не должны были, ждали {deposit_credit_account_response.balance} а там {account_db.balance}"
        assert credit_db.balance == pytest.approx(-CreditDefaults.AMOUNT, abs=0.1), \
            f"долг по кредиту {create_credit_response.credit_id} поменялся хотя не должен был, ждали {-CreditDefaults.AMOUNT} а там {credit_db.balance}"
