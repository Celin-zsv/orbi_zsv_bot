import os

import pytest
import pytest_asyncio
from dotenv import load_dotenv
from sqlalchemy import text
from sqlalchemy.exc import ProgrammingError
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.pool import NullPool

import app.core.config as conf

load_dotenv()
MAIN_DATABASE_URL = conf.settings.database_url
conf.settings.database_url = os.environ.get("TEST_DATABASE_URL")

from app.core.db import Base  # noqa
from app.main import app  # noqa

pytest_plugins = [
    "fixtures.user",
]

main_engine = create_async_engine(MAIN_DATABASE_URL, poolclass=NullPool)


@pytest.fixture(scope="session")
def celery_config():
    return {
        "broker_url": "memory://",
        "task_serializer": "pickle",
        "accept_content": ["application/json", "application/x-python-serialize"],
    }


@pytest.fixture(scope="session")
def celery_worker_parameters():
    return {
        "shutdown_timeout": 3600,
    }


@pytest.fixture(scope="session")
def celery_includes():
    return [
        "app.celery_worker",
    ]


@pytest_asyncio.fixture(autouse=True)
async def init_db_session():
    query = f'CREATE DATABASE {os.environ.get("POSTGRES_TEST_DB")}'
    try:
        async with main_engine.connect() as conn:
            await conn.execution_options(isolation_level="AUTOCOMMIT")
            await conn.execute(text(query))
    except ProgrammingError as error:
        if "DuplicateDatabaseError" not in str(error):
            raise ProgrammingError

    test_engine = create_async_engine(os.environ.get("TEST_DATABASE_URL"), poolclass=NullPool)
    TestingSessionLocal = async_sessionmaker(test_engine)

    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    async with TestingSessionLocal() as session:
        yield session
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
