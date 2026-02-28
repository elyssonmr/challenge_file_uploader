from http import HTTPStatus

import pytest
from fastapi.testclient import TestClient

from file_uploader.app import app
from file_uploader.settings import Settings


@pytest.fixture
def client():
    return TestClient(app)


def test_get_health_check_should_return_ok(client):
    response = client.get('/health')
    settings = Settings()

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'ok', 'version': settings.version}
