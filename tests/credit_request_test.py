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
from api.assertions.credit_assertions import CreditAssert
from api.constants.api_errors import ApiError
from api.constants.credit_constants import CreditDefaults
from api.generators.amount_generator import AmountGenerator


@pytest.mark.api
class TestCredit:
    def test_credit_submission(self,
                               db_session: Session,
                               api_manager: ApiManager,
                               create_credit_user: CreateUserCreditRequest,
                               create_account_credit_response: CreateAccountResponse):
        amount = AmountGenerator.credit()
        response = api_manager.credit_steps.create_credit(user_credit=create_credit_user,
                                                          account_response=create_account_credit_response,
                                                          amount=amount,
                                                          term_months=CreditDefaults.TERM_MONTHS)
        account_db = Account.get_account_by_id(db_session, create_account_credit_response.id)
        credit_db = Credit.get_credit_by_id(db_session, response.credit_id)

        AccountAssert.balance_increased_by(account_db=account_db,
                                           balance_before=create_account_credit_response.balance,
                                           amount=amount)
        BaseAssert.float_equal(actual=response.amount,
                               expected=amount,
                               message=f"сумма кредита в ответе некорректная, "
                                       f"ждали {amount} пришла {response.amount}")
        CreditAssert.debt_in_db(credit_db=credit_db, credit_amount=amount)

    def test_second_credit_submission(self,
                                      db_session: Session,
                                      api_manager: ApiManager,
                                      create_credit_user: CreateUserCreditRequest,
                                      create_account_credit_response: CreateAccountResponse,
                                      create_credit_response: CreditSubmissionResponse):
        response = api_manager.credit_steps.create_credit_invalid(user_credit=create_credit_user,
                                                                  account_response=create_account_credit_response,
                                                                  amount=AmountGenerator.credit(),
                                                                  term_months=CreditDefaults.TERM_MONTHS)
        account_db = Account.get_account_by_id(db_session, create_account_credit_response.id)

        assert response.json()["error"] == ApiError.ONE_ACTIVE_CREDIT, \
            f"бек вернул не ту ошибку: {response.text}"
        AccountAssert.balance_increased_by(account_db=account_db,
                                           balance_before=create_account_credit_response.balance,
                                           amount=create_credit_response.amount)

    def test_credit_repay(self,
                          db_session: Session,
                          api_manager: ApiManager,
                          create_credit_user: CreateUserCreditRequest,
                          create_account_credit_response: CreateAccountResponse,
                          create_credit_response: CreditSubmissionResponse,
                          deposit_credit_account_response: DepositResponse):
        repay_amount = int(create_credit_response.amount)  # по ТЗ кредит гасится только целиком
        response = api_manager.credit_steps.repay_credit(user=create_credit_user,
                                                         account_response=create_account_credit_response,
                                                         credit_response=create_credit_response,
                                                         amount=repay_amount)
        account_db = Account.get_account_by_id(db_session, create_account_credit_response.id)
        credit_db = Credit.get_credit_by_id(db_session, create_credit_response.credit_id)

        BaseAssert.float_equal(actual=response.amount_deposited,
                               expected=repay_amount,
                               message=f"сумма погашения в ответе некорректная, "
                                       f"ждали {repay_amount} пришла {response.amount_deposited}")
        AccountAssert.balance_decreased_by(account_db=account_db,
                                           balance_before=deposit_credit_account_response.balance,
                                           amount=repay_amount)
        CreditAssert.debt_in_db(credit_db=credit_db,
                                credit_amount=create_credit_response.amount,
                                repaid=repay_amount)

    def test_repay_more_than_debt(self,
                                  db_session: Session,
                                  api_manager: ApiManager,
                                  create_credit_user: CreateUserCreditRequest,
                                  create_credit_response: CreditSubmissionResponse,
                                  deposit_credit_account_response: DepositResponse):
        repay_amount = int(create_credit_response.amount) + 1000
        response = api_manager.credit_steps.repay_credit_invalid(user=create_credit_user,
                                                                 account_id=deposit_credit_account_response.id,
                                                                 credit_id=create_credit_response.credit_id,
                                                                 amount=repay_amount)
        account_db = Account.get_account_by_id(db_session, deposit_credit_account_response.id)

        assert response.json()["error"] == ApiError.REPAY_EXCEEDS_DEBT, \
            f"бек вернул не ту ошибку: {response.text}"
        AccountAssert.balance_unchanged(account_db=account_db,
                                        balance_before=deposit_credit_account_response.balance)