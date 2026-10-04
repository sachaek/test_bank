from api.assertions.base_assertions import BaseAssert
from api.db.models.account_table import Account


class AccountAssert:
    @staticmethod
    def assert_balance_in_db(account_db: Account,
                             expected_balance: float,
                             message: str = None) -> None:
        if message is None:
            message = f"баланс аккаунта {account_db.id} в бд некорректный, ждали {expected_balance} а там {account_db.balance}"
        BaseAssert.float_equal(actual=account_db.balance,
                               expected=expected_balance,
                               message=message)

    @staticmethod
    def balance_increased_by(account_db: Account, balance_before: float, amount: float) -> None:
        expected_balance = balance_before + amount
        AccountAssert.assert_balance_in_db(
            account_db=account_db,
            expected_balance=expected_balance,
            message=f"баланс аккаунта {account_db.id} не вырос на {amount}, "
                    f"ждали {expected_balance} а там {account_db.balance}")

    @staticmethod
    def balance_decreased_by(account_db: Account, balance_before: float, amount: float) -> None:
        expected_balance = balance_before - amount
        AccountAssert.assert_balance_in_db(
            account_db=account_db,
            expected_balance=expected_balance,
            message=f"с аккаунта {account_db.id} не списалось {amount}, "
                    f"ждали {expected_balance} а там {account_db.balance}")

    @staticmethod
    def balance_unchanged(account_db: Account, balance_before: float) -> None:
        AccountAssert.assert_balance_in_db(
            account_db=account_db,
            expected_balance=balance_before,
            message=f"баланс аккаунта {account_db.id} поменялся хотя не должен был, "
                    f"ждали {balance_before} а там {account_db.balance}")
