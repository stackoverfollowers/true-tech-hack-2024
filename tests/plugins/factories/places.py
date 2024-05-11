from datetime import UTC, datetime

import factory
import pytest
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from tth.common.constants import MTS_DOMAIN
from tth.common.places.models import PlaceModel, PlaceFromMtsModel
from tth.db.models import Place


class PlaceFactory(factory.Factory):
    class Meta:
        model = Place

    id = factory.Sequence(lambda n: n + 1)
    name = "Das ist Place"
    description = "Das ist eine Beschreibung"
    address = "Die Adresse"
    url = "Some URL"
    image_url = "Some Image URL"
    created_at = factory.LazyFunction(lambda: datetime.now(tz=UTC))
    updated_at = factory.LazyFunction(lambda: datetime.now(tz=UTC))


class PlaceMtsFactory(factory.Factory):
    class Meta:
        model = PlaceFromMtsModel

    id = factory.Sequence(lambda n: n + 1)
    title = "Das ist Place"
    address = "Die Adresse"
    url = MTS_DOMAIN + "/some/url"
    imageUrl = MTS_DOMAIN + "/some-image/url"


@pytest.fixture
def create_place(session: AsyncSession):
    async def _create(**kwargs) -> Place:
        place = PlaceFactory(**kwargs)
        session.add(place)
        await session.commit()
        return place

    return _create

@pytest.fixture
def create_dummy_place_mts():
    def _create(**kwargs) -> PlaceFromMtsModel:
        place = PlaceMtsFactory(**kwargs)
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

