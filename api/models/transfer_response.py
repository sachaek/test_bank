from pydantic import Field

from api.models.base_model import BaseModel


class TransferResponse(BaseModel):
    from_account_id: int = Field(alias="fromAccountId")
    to_account_id: int = Field(alias="toAccountId")
    from_account_id_balance: float = Field(alias="fromAccountIdBalance")