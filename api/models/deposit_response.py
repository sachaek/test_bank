from pydantic import Field

from api.models.base_model import BaseModel


class DepositResponse(BaseModel):
    account_id: int = Field(alias="accountId")
    amount: float  # больше подойдет Decimal, но для простоты используем float