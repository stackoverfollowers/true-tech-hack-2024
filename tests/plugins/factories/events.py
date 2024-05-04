from datetime import UTC, datetime

import factory
import pytest
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from tth.common.events.models import EventModel
from tth.db.models import Event, EventType


class EventFactory(factory.Factory):
    class Meta:
        model = Event

    id = factory.Sequence(lambda n: n + 1)
    place_id = 1
    name = factory.Sequence(lambda n: f"event-{n+1}")
    description = "Description event"
    event_type = EventType.CONCERTS
    url = "Some URL"
    image_url = "Some Image URL"
    started_at = datetime(year=2024, month=1, day=1, tzinfo=UTC)
    ended_at = datetime(year=2024, month=1, day=2, tzinfo=UTC)
    created_at = factory.LazyFunction(lambda: datetime.now(tz=UTC))
    updated_at = factory.LazyFunction(lambda: datetime.now(tz=UTC))


@pytest.fixture
def create_event(session: AsyncSession):
    async def _create(**kwargs) -> Event:
        event = EventFactory(**kwargs)
        session.add(event)
        await session.commit()
        return event

    return _create


@pytest.fixture
def read_event(session: AsyncSession):
    async def _read_event(event_id: int) -> EventModel | None:
        stmt = select(Event).where(Event.id == event_id)
        obj = (await session.scalars(stmt)).first()
        if obj is None:
            return None
        await session.refresh(obj)
        return EventModel.model_validate(obj)

    return _read_event
