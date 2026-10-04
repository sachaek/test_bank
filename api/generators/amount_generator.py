import random

from api.constants.limits import Limits


class AmountGenerator:
    @staticmethod
    def deposit() -> int:
        return random.randint(Limits.DEPOSIT_MIN, Limits.DEPOSIT_MAX)

    @staticmethod
    def credit() -> int:
        return random.randint(Limits.CREDIT_MIN, Limits.CREDIT_MAX)

    @staticmethod
    def transfer(balance: float) -> float:
        max_amount = min(Limits.TRANSFER_MAX, balance)
        amount = random.uniform(Limits.TRANSFER_MIN, max_amount)
        return round(amount, 2)
