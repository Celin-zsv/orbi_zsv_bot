import pytest
from fastapi.testclient import TestClient

from tests.conftest import app


@pytest.fixture(scope="session")
def test_client():
    with TestClient(app) as client:
        yield client
