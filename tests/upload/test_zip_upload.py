from http import HTTPStatus
from unittest.mock import patch
from uuid import uuid4

import pytest
from sqlalchemy import select

from file_uploader.models import ZipUpload


@pytest.fixture
def mock_uuid():
    with patch('file_uploader.upload.routes.uuid4') as patched:
        return_value = uuid4()
        patched.return_value = return_value
        yield return_value


async def test_upload_zip_file_should_save_file(
    client, get_test_asset, mock_uuid, session
):
    filename = 'example1.zip'
    with get_test_asset(filename) as zip_file:
        files = {'file': zip_file}
        response = client.post('/v1/upload/zip', files=files)

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'file_identification': str(mock_uuid)}
    uploaded = await session.scalar(
        select(ZipUpload).where(
            ZipUpload.upload_identification == str(mock_uuid)
        )
    )
    assert uploaded.file_name == filename


def test_upload_non_zip_should_return_error(client, get_test_asset):
    with get_test_asset('cat.png') as upload_file:
        files = {'file': upload_file}

        response = client.post('/v1/upload/zip', files=files)

        assert response.status_code == HTTPStatus.UNSUPPORTED_MEDIA_TYPE
        assert response.json() == {
            'detail': 'Entity body in unsupported format'
        }
