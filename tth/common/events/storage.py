import abc
import asyncio
from collections.abc import Sequence
from dataclasses import dataclass

from sqlalchemy import delete, func, insert, select, union, update
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from tth.common.events.models import (
    CreateEventModel,
    EventFeatureModel,
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


class IEventStorage(abc.ABC):
    @abc.abstractmethod
    async def get_by_id(self, event_id: int) -> EventModel | None:
        raise NotImplementedError

    @abc.abstractmethod
    async def get_by_id_with_features(
        self, event_id: int
    ) -> EventWithFeaturesModel | None:
        raise NotImplementedError

    @abc.abstractmethod
    async def create(
        self,
        new_event: CreateEventModel,
    ) -> EventModel:
        raise NotImplementedError

    @abc.abstractmethod
    async def update(
        self,
        event_id: int,
        update_event: UpdateEventModel,
    ) -> EventModel:
        raise NotImplementedError

    @abc.abstractmethod
    async def delete(self, event_id: int) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    async def pagination(self, limit: int, offset: int) -> EventPaginationModel:
        raise NotImplementedError


@dataclass(frozen=True)
class EventStorage(IEventStorage):
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
