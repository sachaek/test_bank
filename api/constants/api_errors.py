from enum import StrEnum


class ApiError(StrEnum):
    ONE_ACTIVE_CREDIT = "Only one active credit allowed per user"
    REPAY_EXCEEDS_DEBT = "Repayment amount exceeds remaining debt"
