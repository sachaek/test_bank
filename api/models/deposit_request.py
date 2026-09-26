from typing import Annotated

from pydantic import Field, ConfigDict

from api.generators.creation_rule import CreationRule
from api.models.base_model import BaseModel


class DepositRequest(BaseModel):
    account_id: int = Field(alias="accountId")
    amount: float