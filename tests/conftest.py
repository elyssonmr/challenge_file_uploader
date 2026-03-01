import contextlib
import os
from os import path
from pathlib import Path

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from testcontainers.postgres import PostgresContainer

from file_uploader.app import app
from file_uploader.database import get_session
from file_uploader.models import table_registry


@pytest.fixture(scope='session', autouse=True)
def mock_file_upload_folder():
    test_upload_folder = 'uploads'
    assets_path = Path(test_upload_folder)
    assets_path.mkdir(exist_ok=True)
    yield
    for file in assets_path.iterdir():
        os.remove(file)


@pytest.fixture
def get_test_asset():
    @contextlib.contextmanager
    def get_asset(name, mode='rb'):
        curr_dir = path.dirname(path.abspath(__file__))
        with open(f'{curr_dir}/test_assets/{name}', mode) as asset_file:
            yield asset_file

    return get_asset


@pytest.fixture(scope='session')
async def engine():
    with PostgresContainer('postgres:18-alpine', driver='psycopg') as postgres:
        engine = create_async_engine(postgres.get_connection_url())
        yield engine


@pytest.fixture
async def session(engine):
    async with engine.begin() as conn:
        await conn.run_sync(table_registry.metadata.create_all)

    async with AsyncSession(engine, expire_on_commit=False) as session:
        yield session

    async with engine.begin() as conn:
        await conn.run_sync(table_registry.metadata.drop_all)


@pytest.fixture
def client(session):
    def get_session_override():
        return session

    with TestClient(app) as client:
        app.dependency_overrides[get_session] = get_session_override
        yield client

    app.dependency_overrides.clear()
