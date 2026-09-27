from pydantic import Field

from api.models.base_model import BaseModel


class DepositResponse(BaseModel):
    id: int
    balance: float