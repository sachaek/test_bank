from pydantic import Field
from api.models.base_model import BaseModel


class CreditSubmissionResponse(BaseModel):
    account_id: int = Field(alias="accountId")
    amount: float
    term_months: int = Field(alias="termMonths")
    balance: float
    credit_id: int = Field(alias="creditId")