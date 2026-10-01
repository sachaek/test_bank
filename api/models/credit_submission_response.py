from pydantic import Field
from api.models.base_model import BaseModel


class CreditSubmissionResponse(BaseModel):
    id: int = Field(description="AccountId")
    amount: float
    term_months: int = Field(alias="termMonths")
    balance: float
    credit_id: int = Field(alias="creditId")