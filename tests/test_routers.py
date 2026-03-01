from http import HTTPStatus

from file_uploader.settings import Settings


def test_get_health_check_should_return_ok(client):
    response = client.get('/health')
    settings = Settings()

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'ok', 'version': settings.VERSION}
