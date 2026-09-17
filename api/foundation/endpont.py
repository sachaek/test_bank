from dataclasses import dataclass
from typing import Optional, Type
from api.models.base_model import BaseModel


@dataclass
class EndpointConfiguration:
    url: str
    request_model: Optional[Type[BaseModel]]
    response_model: Optional[Type[BaseModel]]

class Endpoint:
