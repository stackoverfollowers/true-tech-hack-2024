import asyncio
import logging
from collections.abc import Iterable, Sequence
from dataclasses import dataclass
from itertools import islice
from typing import Any

from sqlalchemy import delete, func, select, union, update
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from tth.common.events.models import (
    CreateEventModel,
    EventFeatureModel,
    EventFromMtsModel,
    EventModel,
    EventPaginationModel,
    EventWithFeaturesModel,
    UpdateEventModel,
)
from tth.db.models import Event as EventDb
from tth.db.models import EventFeature as EventFeatureDb
from tth.db.models import Feature as FeatureDb
from tth.db.models import PlaceFeature as PlaceFeatureDb
from tth.db.utils import inject_session

log = logging.getLogger(__name__)

INSERT_CHUNK_SIZE = 500


@dataclass(frozen=True)
class EventStorage:
    session_factory: async_sessionmaker[AsyncSession]

    @inject_session
    async def get_by_id(
        self,
        session: AsyncSession,
        event_id: int,
    ) -> EventModel | None:
        obj = await session.get(EventDb, event_id)
        return EventModel.model_validate(obj) if obj else None

    @inject_session
    async def get_by_id_with_features(
        self,
        session: AsyncSession,
        event_id: int,
    ) -> EventWithFeaturesModel | None:
        event = await self.get_by_id(session=session, event_id=event_id)
        if event is None:
            return None
        stmt = union(
            select(
                FeatureDb.id,
                FeatureDb.name,
                FeatureDb.slug,
                EventFeatureDb.value,
            )
            .join(FeatureDb, FeatureDb.id == EventFeatureDb.feature_id)
            .where(EventFeatureDb.event_id == event_id),
            select(
                FeatureDb.id,
                FeatureDb.name,
                FeatureDb.slug,
                PlaceFeatureDb.value,
            )
            .join(FeatureDb, FeatureDb.id == PlaceFeatureDb.feature_id)
            .where(PlaceFeatureDb.place_id == event.place_id),
        )
        result = await session.execute(stmt)
        return EventWithFeaturesModel(
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
            features=[
                EventFeatureModel.model_validate(row._mapping) for row in result.all()
            ],
        )

    @inject_session
    async def create(
        self,
        session: AsyncSession,
        new_event: CreateEventModel,
    ) -> EventModel:
        stmt = (
            insert(EventDb)
            .values(
                place_id=new_event.place_id,
                name=new_event.name,
                url=new_event.url,
                image_url=new_event.image_url,
                event_type=new_event.event_type,
                description=new_event.description,
                started_at=new_event.started_at,
                ended_at=new_event.ended_at,
            )
            .returning(EventDb)
        )
        result = await session.scalars(stmt)
        await session.commit()
        return EventModel.model_validate(result.one())

    @inject_session
    async def update(
        self,
        session: AsyncSession,
        event_id: int,
        update_event: UpdateEventModel,
    ) -> EventModel:
        data = update_event.model_dump(exclude_unset=True)
        stmt = (
            update(EventDb)
            .where(EventDb.id == event_id)
            .values(**data)
            .returning(EventDb)
        )
        result = await session.scalars(stmt)
        await session.commit()
        return EventModel.model_validate(result.one())

    @inject_session
    async def delete(self, session: AsyncSession, event_id: int) -> None:
        await session.execute(delete(EventDb).where(EventDb.id == event_id))
        await session.commit()

    async def pagination(
        self,
        limit: int,
        offset: int,
    ) -> EventPaginationModel:
        total, items = await asyncio.gather(
            self._get_count(),
            self._get_items(
                limit=limit,
                offset=offset,
            ),
        )
        return EventPaginationModel.build(
            limit=limit,
            offset=offset,
            total=total,
            items=items,
        )

    @inject_session
    async def _get_count(
        self,
        session: AsyncSession,
    ) -> int:
        stmt = select(func.count(EventDb.id))
        result = await session.execute(stmt)
        return result.scalar_one()

    @inject_session
    async def _get_items(
        self,
        session: AsyncSession,
        limit: int,
        offset: int,
    ) -> Sequence[EventDb]:
        stmt = select(EventDb).order_by(EventDb.id).offset(offset).limit(limit)
        result = await session.scalars(stmt)
        return result.all()

    @inject_session
    async def save_many_from_mts(
        self,
        session: AsyncSession,
        events: Iterable[EventFromMtsModel],
    ) -> Sequence[int]:
        event_ids: list[int] = []
        for events_chunk in split_every(INSERT_CHUNK_SIZE, events):
            stmt: Any = insert(EventDb).values(
                [
                    {
                        "id": event_data.id,
                        "name": event_data.title,
                        "place_id": event_data.venue.id,
                        "url": event_data.url,
                        "image_url": event_data.image_url,
                        "event_type": event_data.event_type,
                    }
                    for event_data in events_chunk
                ]
            )

            stmt = stmt.on_conflict_do_update(
                index_elements=[EventDb.id],
                set_={
                    "name": stmt.excluded.name,
                    "place_id": stmt.excluded.place_id,
                    "url": stmt.excluded.url,
                    "image_url": stmt.excluded.image_url,
                    "event_type": stmt.excluded.event_type,
                },
            ).returning(EventDb.id)

            result = await session.scalars(stmt)
            event_ids.extend(result.all())

        await session.commit()
        return event_ids


def split_every(n: int, iterable: Iterable) -> Iterable:
    i = iter(iterable)
    piece = list(islice(i, n))
    while piece:
        yield piece
        piece = list(islice(i, n))
