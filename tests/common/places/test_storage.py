from datetime import datetime

import pytest

from tth.common.events.models import (
    CreateEventModel,
    EventModel,
    EventPaginationModel,
    EventWithFeaturesModel,
    UpdateEventModel,
)
from tth.common.events.storage import IEventStorage
from tth.common.places.models import CreatePlaceModel, PlaceModel, PlaceWithFeaturesModel, UpdatePlaceModel, \
    PlacePaginationModel
from tth.common.places.storage import IPlaceStorage


async def test_create_place__ok(
    place_storage: IPlaceStorage,
    read_place,
):
    place = await place_storage.create(
        new_place=CreatePlaceModel(
            name="Test Place",
            description="Test place description",
            address="Test Address",
        )
    )

    assert place == await read_place(place.id)


async def test_get_place_by_id__ok(
    place_storage: IPlaceStorage,
    create_place
):
    place = await create_place()

    assert await place_storage.get_by_id(
        place_id=place.id
    ) == PlaceModel.model_validate(place)


async def test_get_place_by_id__not_found(place_storage: IPlaceStorage):
    assert await place_storage.get_by_id(place_id=1) is None


async def test_get_place_by_id_with_features_not_features__ok(
    place_storage: IPlaceStorage,
    create_place,
):
    place = await create_place()

    assert await place_storage.get_by_id_with_features(
        place_id=place.id
    ) == PlaceWithFeaturesModel(
        id=place.id,
        name=place.name,
        description=place.description,
        address=place.address,
        created_at=place.created_at,
        updated_at=place.updated_at,
        features=[],
    )


async def test_get_place_by_id_with_features__ok(place_storage: IPlaceStorage):
    pass


async def test_get_place_by_id_with_features__not_found(place_storage: IPlaceStorage):
    assert await place_storage.get_by_id_with_features(place_id=1) is None


async def test_update_event__ok(
    place_storage: IPlaceStorage,
    create_place,
    read_place,
):
    place = await create_place()

    await place_storage.update(
        place_id=place.id, update_place=UpdatePlaceModel(name="Updated place name")
    )
    assert (await read_place(place.id)).name == "Updated place name"


async def test_delete_empty_place__ok(place_storage: IPlaceStorage):
    await place_storage.delete(place_id=-1)


async def test_delete_place__ok(
    place_storage: IPlaceStorage,
    create_place,
    read_place,
):
    place = await create_place()

    await place_storage.delete(place_id=place.id)
    assert await read_place(place.id) is None


async def test_pagination__ok(
    place_storage: IPlaceStorage,
    create_place,
):
    places = [await create_place() for _ in range(3)]
    pagination = await place_storage.pagination(limit=10, offset=1)
    assert pagination == PlacePaginationModel.build(
        limit=10, offset=1, total=3, items=places[1:]
    )


async def test_pagination_empty__ok(place_storage: IPlaceStorage):
    pagination = await place_storage.pagination(limit=10, offset=0)
    assert pagination == PlacePaginationModel.build(
        limit=10, offset=0, total=0, items=[]
    )


@pytest.mark.parametrize(("limit", "result"), ((0, 0), (3, 3), (5, 3)))
async def test_pagination_limit__ok(
    place_storage: IPlaceStorage,
    limit: int,
    result: int,
    create_place
):
    [await create_place() for _ in range(3)]
    pagination = await place_storage.pagination(limit=limit, offset=0)
    assert len(pagination.items) == result


@pytest.mark.parametrize(("offset", "result"), ((0, 4), (3, 1), (5, 0)))
async def test_pagination_offset__ok(
    place_storage: IPlaceStorage,
    offset: int,
    result: int,
    create_place,
):
    [await create_place() for _ in range(4)]
    pagination = await place_storage.pagination(limit=10, offset=offset)
    assert len(pagination.items) == result
