"""Shared test fixtures: a real Postgres test database, one rolled-back transaction per test."""

import os
from collections.abc import AsyncIterator

import httpx
import pytest
from sqlalchemy.ext.asyncio import AsyncConnection, AsyncSession, create_async_engine

from kb_api.config import get_settings
from kb_api.db import get_session
from kb_api.main import create_app
from kb_api.models import Base

TEST_DATABASE_URL = os.environ.get("TEST_DATABASE_URL", "postgresql+asyncpg://kb:kb@localhost:5432/kb_test")


@pytest.fixture(scope="session")
def anyio_backend() -> str:
    return "asyncio"


@pytest.fixture(scope="session")
async def connection() -> AsyncIterator[AsyncConnection]:
    """Create the schema once per test run (like db:test:prepare)."""
    engine = create_async_engine(TEST_DATABASE_URL)
    async with engine.connect() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
        await conn.commit()
        yield conn
    await engine.dispose()


@pytest.fixture
async def session(connection: AsyncConnection) -> AsyncIterator[AsyncSession]:
    """Each test runs inside a transaction that is rolled back (like use_transactional_fixtures)."""
    transaction = await connection.begin()
    session = AsyncSession(bind=connection, join_transaction_mode="create_savepoint", expire_on_commit=False)
    yield session
    await session.close()
    await transaction.rollback()


@pytest.fixture
async def client(session: AsyncSession) -> AsyncIterator[httpx.AsyncClient]:
    """An HTTP client that calls the app in memory (no server), using the test session."""
    app = create_app()

    async def override_session() -> AsyncIterator[AsyncSession]:
        yield session

    app.dependency_overrides[get_session] = override_session
    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as c:
        yield c


@pytest.fixture
def auth() -> dict[str, str]:
    return {"X-API-Key": get_settings().api_key.get_secret_value()}
