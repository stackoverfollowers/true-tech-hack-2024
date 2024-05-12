import pytest
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from tth.common.events.storage import EventStorage


@pytest.fixture
def event_storage(
    session_factory: async_sessionmaker[AsyncSession],
) -> EventStorage:
    return EventStorage(session_factory=session_factory)
