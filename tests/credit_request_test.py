from sqlalchemy.orm import Session

from api.classes.api_manager import ApiManager
from api.models.create_account_response import CreateAccountResponse
from api.models.create_user_request import CreateUserCreditRequest


class TestCredit:
    def test_credit_submission(self,
                               db_session: Session,
                               api_manager: ApiManager,
                               create_credit_user: CreateUserCreditRequest,
                               create_account_credit_response: CreateAccountResponse):
        response = api_manager.credit_steps.create_credit(user_credit=create_credit_user,
                                                          account_response=create_account_credit_response)
