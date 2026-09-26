from typing import Annotated

from pydantic import Field, ConfigDict

from api.generators.creation_rule import CreationRule
from api.models.base_model import BaseModel


class DepositRequest(BaseModel):
    account_id: int = Field(alias="accountId")
    amount: Annotated[float, CreationRule(regex=r'^(?:[1-8]\d{3}(?:\.\d+)?|9000(?:\.0+)?)$')]