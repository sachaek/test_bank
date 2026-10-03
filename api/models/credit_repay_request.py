from pydantic import Field
from api.models.base_model import BaseModel


class CreditRepayRequest(BaseModel):
    credit_id: int = Field(alias="creditId")
    account_id: int = Field(alias="accountId")
    amount: int = Field(alias="amount")