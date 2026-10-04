import pytest


class BaseAssert:
    @staticmethod
    def float_equal(actual, expected, tolerance: float = 0.1, message=None):
        if not message:
            message = f"значение {actual} не равно {expected} с точностью {tolerance}"
        assert actual == pytest.approx(expected, abs=tolerance), message
