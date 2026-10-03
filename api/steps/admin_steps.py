import allure

from api.foundation.endpont import Endpoint
from api.foundation.requester.crud_requester import CrudRequester
from api.foundation.requester.validate_crud_requester import ValidateCrudRequester
from api.models.create_user_request import CreateUserRequest
from api.models.login_user_requests import LoginUserRequest
from api.steps.base_steps import BaseSteps
from specs.request_specs import RequestSpecs
from specs.response_specs import ResponseSpecs


class AdminSteps(BaseSteps):
    @allure.step("Создание пользователя админом")
    def create_user(self, create_user_request: CreateUserRequest):
        response = ValidateCrudRequester(
            request_spec=RequestSpecs.auth_headers(username="admin", password="123456"),
            endpoint=Endpoint.ADMIN_CREATE_USER,
            response_spec=ResponseSpecs.request_ok()
        ).post(create_user_request)

        self.created_obj.append(response)
        return response

    @allure.step("Удаление пользователя с id {user_id} админом")
    def delete_user(self, user_id: int):
        CrudRequester(
            request_spec=RequestSpecs.auth_headers(username="admin", password="123456"),
            endpoint=Endpoint.ADMIN_DELETE_USER,
            response_spec=ResponseSpecs.request_ok()
        ).delete(user_id)

    @allure.step("Невалидное создание пользователя админом")
    def create_invalid_user(self, create_user_request: CreateUserRequest):
        CrudRequester(
            request_spec=RequestSpecs.auth_headers(username="admin", password="123456"),
            endpoint=Endpoint.ADMIN_CREATE_USER,
            response_spec=ResponseSpecs.request_bad()
        ).post(create_user_request)

    @allure.step("Логин пользователя")
    def login_user(self, login_user_request: LoginUserRequest):
        response = ValidateCrudRequester(
            request_spec=RequestSpecs.unauth_headers(),
            endpoint=Endpoint.LOGIN_USER,
            response_spec=ResponseSpecs.request_ok()
        ).post(login_user_request)
        return response