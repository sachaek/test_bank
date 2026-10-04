from api.assertions.base_assertions import BaseAssert
from api.db.models.credit_table import Credit


class CreditAssert:
    @staticmethod
    def debt_in_db(credit_db: Credit | None, credit_amount: float, repaid: float = 0) -> None:
        """Долг хранится в бд отрицательным балансом: -(сумма кредита - погашено)."""
        assert credit_db is not None, "кредита нет в бд"
        expected_debt = -(credit_amount - repaid)
        BaseAssert.float_equal(actual=credit_db.balance,
                               expected=expected_debt,
                               message=f"долг по кредиту {credit_db.id} в бд некорректный, "
                                       f"ждали {expected_debt} а там {credit_db.balance}")
