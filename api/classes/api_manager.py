from typing import List, Any

from api.steps.admin_steps import AdminSteps
from api.steps.user_credit_steps import UserCreditSteps
from api.steps.user_stpes import UserSteps


class ApiManager:
    def __init__(self, created_obj: List[Any]):
        self.admin_steps = AdminSteps(created_obj)
        self.user_steps = UserSteps(created_obj)
        self.credit_steps = UserCreditSteps(created_obj)