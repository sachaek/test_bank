import pytest

pytest.register_assert_rewrite("api.assertions")  # до импортов, чтобы pytest мог переписать assert в этих модулях

from api.fixtures.api_fixture import *
from api.fixtures.admin_fixture import *
from api.fixtures.object_fixture import *
from api.fixtures.user_fixture import *
from api.fixtures.credit_fixtures import *
from api.fixtures.db_fixture import *