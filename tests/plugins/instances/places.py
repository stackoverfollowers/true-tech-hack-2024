import pytest
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from tth.common.places.storage import PlaceStorage, IPlaceStorage


@pytest.fixture
def place_storage(
    session_factory: async_sessionmaker[AsyncSession],
) -> IPlaceStorage:
    return PlaceStorage(session_factory=session_factory)
