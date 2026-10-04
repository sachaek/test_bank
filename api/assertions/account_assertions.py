from sqlalchemy.orm import Session
from api.assertions.base_assertions import BaseAssert
from api.db.crud.account_crud import AccountCrudDB


class AccountAssert:
    @staticmethod
    def assert_balance_in_db(account_db: AccountCrudDB,
                             expected_balance: float,
                             account_id: int,
                             message: str = None) -> None:
        if message is None:
            message = f"баланс аккаунта {account_id} в бд не вырос, ждали {expected_balance} а там {account_db.balance}"
        balance = account_db.balance
        BaseAssert.float_equal(
            actual=balance,
            expected=expected_balance,
            message=message
        )