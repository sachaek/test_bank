from typing import Annotated

from api.generators.creation_rule import CreationRule
from api.models.base_model import BaseModel


class CreateUserRequest(BaseModel):
    username: Annotated[str, CreationRule(regex=r'^[A-Za-z0-9]{3,15}$')]
    password: Annotated[str, CreationRule(regex=r'^[A-Z]{3}[a-z]{1}[0-9]{2}[!$_]{4}$')]
    role: Annotated[str, CreationRule(regex=r'^ROLE_USER')]