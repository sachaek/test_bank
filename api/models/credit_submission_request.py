from pydantic import Field
from api.models.base_model import BaseModel


class CreditSubmissionRequest(BaseModel):
    account_id: int = Field(alias="accountId")
    amount: float
    termMonths: int = Field(alias="termMonths")