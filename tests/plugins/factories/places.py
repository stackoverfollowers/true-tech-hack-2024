from datetime import UTC, datetime

import factory
import pytest
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from tth.common.places.models import PlaceModel
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


@pytest.fixture
def read_place(session: AsyncSession):
    async def _read_place(place_id: int) -> PlaceModel | None:
        stmt = select(Place).where(Place.id == place_id)
        obj = (await session.scalars(stmt)).first()
        if obj is None:
            return None
        await session.refresh(obj)
        return PlaceModel.model_validate(obj)

    return _read_place

