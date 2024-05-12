import pytest

from tests.plugins.factories.places import PlaceMtsFactory
from tth.common.places.models import (
    CreatePlaceModel,
    PlaceModel,
    PlacePaginationModel,
    PlaceWithFeaturesModel,
    UpdatePlaceModel,
)
from tth.common.places.storage import PlaceStorage


async def test_create_place__ok(
    place_storage: PlaceStorage,
    read_place,
):
    place = await place_storage.create(
        new_place=CreatePlaceModel(
            name="Test Place",
            description="Test place description",
            address="Test Address",
            url="Test URL",
            image_url="Test Image URL",
        )
    )

    assert place == await read_place(place.id)


async def test_get_place_by_id__ok(place_storage: PlaceStorage, create_place):
    place = await create_place()

    assert await place_storage.get_by_id(
        place_id=place.id
    ) == PlaceModel.model_validate(place)


async def test_get_place_by_id__not_found(place_storage: PlaceStorage):
    assert await place_storage.get_by_id(place_id=1) is None


async def test_get_place_by_id_with_features_not_features__ok(
    place_storage: PlaceStorage,
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
        url=place.url,
        image_url=place.image_url,
        created_at=place.created_at,
        updated_at=place.updated_at,
        features=[],
    )


async def test_get_place_by_id_with_features__ok(place_storage: PlaceStorage):
    pass


async def test_get_place_by_id_with_features__not_found(place_storage: PlaceStorage):
    assert await place_storage.get_by_id_with_features(place_id=1) is None


async def test_update_event__ok(
    place_storage: PlaceStorage,
    create_place,
    read_place,
):
    place = await create_place()

    await place_storage.update(
        place_id=place.id, update_place=UpdatePlaceModel(name="Updated place name")
    )
    assert (await read_place(place.id)).name == "Updated place name"


async def test_delete_empty_place__ok(place_storage: PlaceStorage):
    await place_storage.delete(place_id=-1)


async def test_delete_place__ok(
    place_storage: PlaceStorage,
    create_place,
    read_place,
):
    place = await create_place()

    await place_storage.delete(place_id=place.id)
    assert await read_place(place.id) is None


async def test_pagination__ok(
    place_storage: PlaceStorage,
    create_place,
):
    places = [await create_place() for _ in range(3)]
    pagination = await place_storage.pagination(limit=10, offset=1)
    assert pagination == PlacePaginationModel.build(
        limit=10, offset=1, total=3, items=places[1:]
    )


async def test_pagination_empty__ok(place_storage: PlaceStorage):
    pagination = await place_storage.pagination(limit=10, offset=0)
    assert pagination == PlacePaginationModel.build(
        limit=10, offset=0, total=0, items=[]
    )


@pytest.mark.parametrize(("limit", "result"), ((0, 0), (3, 3), (5, 3)))
async def test_pagination_limit__ok(
    place_storage: PlaceStorage, limit: int, result: int, create_place
):
    [await create_place() for _ in range(3)]
    pagination = await place_storage.pagination(limit=limit, offset=0)
    assert len(pagination.items) == result


@pytest.mark.parametrize(("offset", "result"), ((0, 4), (3, 1), (5, 0)))
async def test_pagination_offset__ok(
    place_storage: PlaceStorage,
    offset: int,
    result: int,
    create_place,
):
    [await create_place() for _ in range(4)]
    pagination = await place_storage.pagination(limit=10, offset=offset)
    assert len(pagination.items) == result


async def test_save_many_from_mts__save_one(
    place_storage: PlaceStorage,
):
    place_from_mts = PlaceMtsFactory()
    await place_storage.save_many_from_mts([place_from_mts])

    saved_place = await place_storage.get_by_id(place_id=place_from_mts.id)

    assert saved_place.id == place_from_mts.id
    assert saved_place.name == place_from_mts.title
    assert saved_place.url == place_from_mts.url
    assert saved_place.image_url == place_from_mts.image_url
    assert saved_place.address == place_from_mts.address


async def test_save_many_from_mts__ok(
    place_storage: PlaceStorage,
):
    places_from_mts = [PlaceMtsFactory() for _ in range(3)]
    places_ids = [p.id for p in places_from_mts]

    saved_places_ids = await place_storage.save_many_from_mts(places_from_mts)

    assert set(saved_places_ids) == set(places_ids)

    for place_to_save in places_from_mts:
        place_in_db = await place_storage.get_by_id(place_id=place_to_save.id)

        assert place_in_db.url == place_to_save.url
        assert place_in_db.image_url == place_to_save.image_url
        assert place_in_db.name == place_to_save.title
        assert place_in_db.address == place_to_save.address


async def test_save_many_from_mts__with_conflict(
    place_storage,
    create_place,
):
    existing_place = await create_place()
    place_from_mts = PlaceMtsFactory(id=existing_place.id)

    updated_place_ids = await place_storage.save_many_from_mts([place_from_mts])

    updated_place = await place_storage.get_by_id(place_id=updated_place_ids[0])

    assert updated_place.id == place_from_mts.id
    assert updated_place.url == place_from_mts.url
    assert updated_place.image_url == place_from_mts.image_url
    assert updated_place.name == place_from_mts.title
    assert updated_place.address == place_from_mts.address
    assert updated_place.description == existing_place.description
