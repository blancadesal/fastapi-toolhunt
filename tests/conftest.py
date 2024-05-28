import os

import pytest
from starlette.testclient import TestClient

from toolhunt.config import Settings, get_settings
from toolhunt.main import create_app


def get_settings_override():
    return Settings(testing=1, database_url=os.getenv("DATABASE_TEST_URL"))


@pytest.fixture(scope="module")
def test_app():
    app = create_app()
    app.dependency_overrides[get_settings] = get_settings_override
    with TestClient(app) as test_client:
        yield test_client
