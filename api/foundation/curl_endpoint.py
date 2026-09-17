from typing import Protocol, Optional
from requests import Response
from api.models.base_model import BaseModel


class CrudEndpoint(Protocol):
    def post(self, model: Optional[BaseModel]) -> BaseModel | Response: ...

    def get(self, user_id: Optional[BaseModel]) -> BaseModel | Response: ...

    def delete(self, user_id: Optional[BaseModel]) -> BaseModel | Response: ...