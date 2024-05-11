from datetime import datetime

import pytest

from tests.plugins.factories.events import EventMtsFactory
from tth.common.events.models import (
    CreateEventModel,
    EventModel,
    EventPaginationModel,
    EventWithFeaturesModel,
    UpdateEventModel,
)
from tth.common.events.storage import IEventStorage
from tth.db.models import EventType


async def test_create_event__ok(
    event_storage: IEventStorage,
    read_event,
    create_place,
):
    place = await create_place()
    event = await event_storage.create(
        new_event=CreateEventModel(
            place_id=place.id,
            name="Test Event",
            event_type=EventType.CONCERTS,
            url="Test URL",
            image_url="Test Image URL",
            description="Very test event",
            started_at=datetime.now(),
            ended_at=datetime.now(),
        )
    )
    assert event == await read_event(event.id)


async def test_get_event_by_id__ok(
    event_storage: IEventStorage, create_event, create_place
):
    place = await create_place()
    event = await create_event(
        place_id=place.id,
    )
    assert await event_storage.get_by_id(
        event_id=event.id
    ) == EventModel.model_validate(event)


async def test_get_event_by_id__not_found(event_storage: IEventStorage):
    assert await event_storage.get_by_id(event_id=1) is None


async def test_get_event_by_id_with_features_not_features__ok(
    event_storage: IEventStorage, create_place, create_event
):
    place = await create_place()
    event = await create_event(
        place_id=place.id,
    )
    assert await event_storage.get_by_id_with_features(
        event_id=event.id
    ) == EventWithFeaturesModel(
        id=event.id,
        place_id=event.place_id,
        name=event.name,
        url=event.url,
        image_url=event.image_url,
        event_type=event.event_type,
        description=event.description,
        started_at=event.started_at,
        ended_at=event.ended_at,
        created_at=event.created_at,
        updated_at=event.updated_at,
        features=[],
    )


async def test_get_event_by_id_with_features__ok(event_storage: IEventStorage):
    pass


async def test_get_event_by_id_with_features__not_found(event_storage: IEventStorage):
    assert await event_storage.get_by_id_with_features(event_id=1) is None


async def test_update_event__ok(
    event_storage: IEventStorage, create_place, create_event, read_event
):
    place = await create_place()
    event = await create_event(
        place_id=place.id,
        name="Old event name",
    )
    await event_storage.update(
        event_id=event.id, update_event=UpdateEventModel(name="New event name")
    )
    assert (await read_event(event.id)).name == "New event name"


async def test_delete_empty_event__ok(event_storage: IEventStorage):
    await event_storage.delete(event_id=-1)


async def test_delete_event__ok(
    event_storage: IEventStorage, create_place, create_event, read_event
):
    place = await create_place()
    event = await create_event(
        place_id=place.id,
    )
    await event_storage.delete(event_id=event.id)
    assert await read_event(event.id) is None


async def test_pagination__ok(event_storage: IEventStorage, create_place, create_event):
    place = await create_place()
    events = [await create_event(place_id=place.id) for _ in range(3)]
    pagination = await event_storage.pagination(limit=10, offset=1)
    assert pagination == EventPaginationModel.build(
        limit=10, offset=1, total=3, items=events[1:]
    )


async def test_pagination_empty__ok(event_storage: IEventStorage):
    pagination = await event_storage.pagination(limit=10, offset=0)
    assert pagination == EventPaginationModel.build(
        limit=10, offset=0, total=0, items=[]
    )


@pytest.mark.parametrize(("limit", "result"), ((0, 0), (3, 3), (5, 3)))
async def test_pagination_limit__ok(
    event_storage: IEventStorage,
    limit: int,
    result: int,
    create_place,
    create_event,
):
    place = await create_place()
    [await create_event(place_id=place.id) for _ in range(3)]
    pagination = await event_storage.pagination(limit=limit, offset=0)
    assert len(pagination.items) == result


@pytest.mark.parametrize(("offset", "result"), ((0, 4), (3, 1), (5, 0)))
async def test_pagination_offset__ok(
    event_storage: IEventStorage,
    offset: int,
    result: int,
    create_place,
    create_event,
):
    place = await create_place()
    [await create_event(place_id=place.id) for _ in range(4)]
    pagination = await event_storage.pagination(limit=10, offset=offset)
    assert len(pagination.items) == result


# async def test_save_many_from_mts__save_one(
#     event_storage: IEventStorage,
#     create_place,
# ):
#     place = await create_place()
#     event_from_mts = EventMtsFactory()
#     event_from_mts.venue.id = place.id
#
#     await event_storage.save_many_from_mts(events=[event_from_mts])
#
#     saved_event = await event_storage.get_by_id(event_id=event_from_mts.id)
#
#     assert saved_event.id == event_from_mts.id
#     assert saved_event.name == event_from_mts.title
#     assert saved_event.url == event_from_mts.url
#     assert saved_event.image_url == event_from_mts.image_url
#     assert saved_event.place_id == event_from_mts.venue.id
#
#
# async def test_save_many_from_mts__ok(
#     event_storage: IEventStorage,
#     create_place
# ):
#     place = await create_place()
#     events_from_mts = [EventMtsFactory() for _ in range(3)]
#     events_ids = [e.id for e in events_from_mts]
#
#     saved_event_ids = await event_storage.save_many_from_mts(
#         events=events_from_mts
#     )
#     assert set(saved_event_ids) == set(events_ids)
#     for event_to_save in events_from_mts:
#         event_in_db = await event_storage.get_by_id(event_id=event_to_save.id)
#         assert event_in_db.url == event_to_save.url
#         assert event_in_db.image_url == event_to_save.image_url
#         assert event_in_db.name == event_to_save.title
#         assert event_in_db.event_type == event_to_save.event_type
#
#
# async def test_save_many_from_mts__with_conflict(
#     event_storage,
#     create_place,
#     create_event,
# ):
#     place = await create_place()
#     another_place = await create_place()
#     existing_event = await create_event()
#
#     event_from_mts = EventMtsFactory(id=existing_event.id)
#     event_from_mts.venue.id = another_place.id
#
#     updated_event_ids = await event_storage.save_many_from_mts(
#         events=[event_from_mts]
#     )
#
#     updated_event = await event_storage.get_by_id(
#         event_id=updated_event_ids[0])
#
#     assert updated_event.id == event_from_mts.id
#     assert updated_event.place_id == event_from_mts.venue.id
#     assert updated_event.url == event_from_mts.url
#     assert updated_event.image_url == event_from_mts.image_url
#     assert updated_event.name == event_from_mts.title
#     assert updated_event.event_type == event_from_mts.event_type
#
#     assert updated_event.place_id != existing_event.place_id
#     assert updated_event.description == existing_event.description
#     assert updated_event.started_at == existing_event.started_at
#     assert updated_event.ended_at == existing_event.ended_at
