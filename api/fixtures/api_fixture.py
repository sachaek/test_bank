import pytest

from api.classes.api_manager import ApiManager


@pytest.fixture()
def api_manager(created_obj):
    return ApiManager(created_obj)