from typing import AsyncGenerator

import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    create_async_engine,
)

from app.api.deps import get_db
from app.main import app
from app.models.genre import Genre
from tests.utils.db import (
    TEST_DB_URL,
    create_test_db,
    drop_test_db,
    run_test_migrations,
)
from tests.utils.genre import create_test_genres


@pytest_asyncio.fixture(name="engine", scope="session")
async def engine_fixture() -> AsyncGenerator[AsyncEngine, None]:
    await create_test_db()
    run_test_migrations(TEST_DB_URL)
    async_engine = create_async_engine(TEST_DB_URL)

    yield async_engine

    await async_engine.dispose()
    await drop_test_db()


@pytest_asyncio.fixture(name="session")
async def session_fixture(engine: AsyncEngine) -> AsyncGenerator[AsyncSession, None]:
    async with engine.connect() as connection:
        transaction = await connection.begin()
        try:
            async with AsyncSession(
                bind=connection,
                expire_on_commit=False,
                join_transaction_mode="create_savepoint",
            ) as session:
                yield session
        finally:
            await transaction.rollback()


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
