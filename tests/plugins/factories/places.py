from datetime import UTC, datetime

import factory
import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from tth.db.models import Place


class PlaceFactory(factory.Factory):
    class Meta:
        model = Place

    id = factory.Sequence(lambda n: n + 1)
    name = "Das ist Place"
    description = "Das ist eine Beschreibung"
    address = "Die Adresse"
    created_at = factory.LazyFunction(lambda: datetime.now(tz=UTC))
    updated_at = factory.LazyFunction(lambda: datetime.now(tz=UTC))


@pytest.fixture
def create_place(session: AsyncSession):
    async def _create(**kwargs) -> Place:
        place = PlaceFactory(**kwargs)
        session.add(place)
        await session.commit()
        return place

    return _create
