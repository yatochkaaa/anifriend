from typing import AsyncGenerator

import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.api.deps import get_db
from app.main import app
from app.models.genre import Genre
from tests.utils.db import (
    TEST_DB_URL,
    create_test_db,
    drop_test_db,
    make_test_migrations,
)
from tests.utils.genre import create_test_genres


@pytest_asyncio.fixture(name="session")
async def session_fixture() -> AsyncGenerator[AsyncSession, None]:
    await create_test_db()
    async_engine = create_async_engine(TEST_DB_URL)
    async_session_maker = async_sessionmaker(async_engine, expire_on_commit=False)
    make_test_migrations(TEST_DB_URL)

    async with async_session_maker() as session:
        yield session

    await async_engine.dispose()
    await drop_test_db()


@pytest_asyncio.fixture(name="client")
async def client_fixture(session: AsyncSession) -> AsyncGenerator[AsyncClient, None]:
    async def get_session_override() -> AsyncGenerator[AsyncSession, None]:
        yield session

    app.dependency_overrides[get_db] = get_session_override

    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        yield ac

    app.dependency_overrides.clear()


@pytest_asyncio.fixture(name="genres")
async def genres_fixture(session: AsyncSession) -> list[Genre]:
    return await create_test_genres(session)
