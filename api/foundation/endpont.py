from dataclasses import dataclass
from typing import Optional, Type
from api.models.base_model import BaseModel
from api.models.create_user_request import CreateUserRequest
from api.models.create_user_response import CreateUserResponse


@dataclass
class EndpointConfiguration:
    url: str
    request_model: Optional[Type[BaseModel]]
    response_model: Optional[Type[BaseModel]]


class Endpoint:
    ADMIN_CREATE_USER = EndpointConfiguration(
        request_model=CreateUserRequest,
        url="/admin/create",
        response_model=CreateUserResponse
    )
