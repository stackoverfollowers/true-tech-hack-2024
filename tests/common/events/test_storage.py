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
