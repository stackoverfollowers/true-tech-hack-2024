import abc
from collections.abc import Sequence
from dataclasses import dataclass

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from tth.common.disabilities.models import Disability
from tth.common.reduce_cache import (
    ReduceCacheMixin,
    reduce_cache,
)
from tth.db.models import (
    Disability as DisabilityDb,
)
from tth.db.models import (
    EventDisability as EventDisabilityDb,
)
from tth.db.models import (
    PlaceDisability as PlaceDisabilityDb,
)
from tth.db.models import (
    UserDisability as UserDisabilityDb,
)
from tth.db.utils import IStorage, inject_session


class IDisabilityStorage(abc.ABC):
    async def get_user_disabilities(self, user_id: int) -> Sequence[Disability]:
        raise NotImplementedError

    async def get_full_event_disabilities(
        self, event_id: int, place_id: int
    ) -> Sequence[Disability]:
        raise NotImplementedError


@dataclass(frozen=True)
class DisabilityStorage(IDisabilityStorage, IStorage):
    session_factory: async_sessionmaker[AsyncSession]

    @inject_session
    async def get_full_event_disabilities(
        self,
        session: AsyncSession,
        event_id: int,
        place_id: int,
    ) -> Sequence[Disability]:
        event_disabilities = await self._get_event_disabilities(session, event_id)
        place_disabilities = await self._get_place_disabilities(session, place_id)
        return tuple(set(event_disabilities) | set(place_disabilities))

    @inject_session
    async def get_user_disabilities(
        self,
        session: AsyncSession,
        user_id: int,
    ) -> Sequence[Disability]:
        stmt = (
            select(DisabilityDb)
            .join(UserDisabilityDb, UserDisabilityDb.disability_id == DisabilityDb.id)
            .where(UserDisabilityDb.user_id == user_id)
        )
        result = (await session.scalars(stmt)).all()
        return tuple(Disability.build(obj) for obj in result)

    @inject_session
    async def _get_event_disabilities(
        self,
        session: AsyncSession,
        event_id: int,
    ) -> Sequence[Disability]:
        stmt = (
            select(DisabilityDb)
            .join(EventDisabilityDb, EventDisabilityDb.disability_id == DisabilityDb.id)
            .where(EventDisabilityDb.event_id == event_id)
        )
        result = (await session.scalars(stmt)).all()
        return tuple(Disability.build(obj) for obj in result)

    @inject_session
    async def _get_place_disabilities(
        self,
        session: AsyncSession,
        place_id: int,
    ) -> Sequence[Disability]:
        stmt = (
            select(DisabilityDb)
            .join(PlaceDisabilityDb, PlaceDisabilityDb.disability_id == DisabilityDb.id)
            .where(PlaceDisabilityDb.place_id == place_id)
        )
        result = (await session.scalars(stmt)).all()
        return tuple(Disability.build(obj) for obj in result)


class DisabilityCachedStorage(IDisabilityStorage, ReduceCacheMixin):
    _storage: DisabilityStorage

    def __init__(self, storage: DisabilityStorage) -> None:
        super().__init__()
        self._storage = storage

    async def get_full_event_disabilities(
        self, event_id: int, place_id: int
    ) -> Sequence[Disability]:
        event_disabilities = await self._get_event_disabilities(event_id)
        place_disabilities = await self._get_place_disabilities(place_id)
        return tuple(set(event_disabilities) | set(place_disabilities))

    @reduce_cache
    async def _get_event_disabilities(self, event_id: int) -> Sequence[Disability]:
        return await self._storage._get_event_disabilities(event_id=event_id)

    @reduce_cache
    async def _get_place_disabilities(self, place_id: int) -> Sequence[Disability]:
        return await self._storage._get_place_disabilities(place_id=place_id)

    @reduce_cache
    async def get_user_disabilities(self, user_id: int) -> Sequence[Disability]:
        return await self._storage.get_user_disabilities(user_id=user_id)
