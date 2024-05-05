import abc
import asyncio
from collections.abc import Sequence
from dataclasses import dataclass

from sqlalchemy import delete, func, insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from tth.common.places.models import (
    CreatePlaceModel,
    PlaceFeatureModel,
    PlaceModel,
    PlacePaginationModel,
    PlaceWithFeaturesModel,
    UpdatePlaceModel,
)
from tth.db.models import Feature as FeatureDb
from tth.db.models import Place as PlaceDb
from tth.db.models import PlaceFeature as PlaceFeatureDb
from tth.db.utils import inject_session


class IPlaceStorage(abc.ABC):
    @abc.abstractmethod
    async def get_by_id(self, place_id: int) -> PlaceModel | None:
        raise NotImplementedError

    @abc.abstractmethod
    async def get_by_id_with_features(
        self, place_id: int
    ) -> PlaceWithFeaturesModel | None:
        raise NotImplementedError

    @abc.abstractmethod
    async def create(
        self,
        new_place: CreatePlaceModel,
    ) -> PlaceModel:
        raise NotImplementedError

    @abc.abstractmethod
    async def update(
        self,
        place_id: int,
        update_place: UpdatePlaceModel,
    ) -> PlaceModel:
        raise NotImplementedError

    @abc.abstractmethod
    async def delete(self, place_id: int) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    async def pagination(self, limit: int, offset: int) -> PlacePaginationModel:
        raise NotImplementedError


@dataclass(frozen=True)
class PlaceStorage(IPlaceStorage):
    session_factory: async_sessionmaker[AsyncSession]

    @inject_session
    async def get_by_id(
        self,
        session: AsyncSession,
        place_id: int,
    ) -> PlaceModel | None:
        obj = await session.get(PlaceDb, place_id)
        return PlaceModel.model_validate(obj) if obj else None

    @inject_session
    async def get_by_id_with_features(
        self,
        session: AsyncSession,
        place_id: int,
    ) -> PlaceWithFeaturesModel | None:
        place = await self.get_by_id(session=session, place_id=place_id)
        if place is None:
            return None
        stmt = (
            select(
                FeatureDb.id,
                FeatureDb.name,
                FeatureDb.slug,
                PlaceFeatureDb.value,
            )
            .join(FeatureDb, FeatureDb.id == PlaceFeatureDb.feature_id)
            .where(PlaceFeatureDb.place_id == place_id)
        )
        result = await session.execute(stmt)
        return PlaceWithFeaturesModel(
            id=place.id,
            name=place.name,
            description=place.description,
            address=place.address,
            created_at=place.created_at,
            updated_at=place.updated_at,
            features=[
                PlaceFeatureModel.model_validate(row._mapping) for row in result.all()
            ],
        )

    @inject_session
    async def create(
        self,
        session: AsyncSession,
        new_place: CreatePlaceModel,
    ) -> PlaceModel:
        stmt = (
            insert(PlaceDb)
            .values(
                name=new_place.name,
                description=new_place.description,
                address=new_place.address
            )
            .returning(PlaceDb)
        )
        result = await session.scalars(stmt)
        await session.commit()
        return PlaceModel.model_validate(result.one())

    @inject_session
    async def update(
        self,
        session: AsyncSession,
        place_id: int,
        update_place: UpdatePlaceModel,
    ) -> PlaceModel:
        data = update_place.model_dump(exclude_unset=True)
        stmt = (
            update(PlaceDb)
            .where(PlaceDb.id == place_id)
            .values(**data)
            .returning(PlaceDb)
        )
        result = await session.scalars(stmt)
        await session.commit()
        return PlaceModel.model_validate(result.one())

    @inject_session
    async def delete(self, session: AsyncSession, place_id: int) -> None:
        await session.execute(delete(PlaceDb).where(PlaceDb.id == place_id))
        await session.commit()

    async def pagination(
        self,
        limit: int,
        offset: int,
    ) -> PlacePaginationModel:
        total, items = await asyncio.gather(
            self._get_count(),
            self._get_items(
                limit=limit,
                offset=offset,
            ),
        )
        return PlacePaginationModel.build(
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
        stmt = select(func.count(PlaceDb.id))
        result = await session.execute(stmt)
        return result.scalar_one()

    @inject_session
    async def _get_items(
        self,
        session: AsyncSession,
        limit: int,
        offset: int,
    ) -> Sequence[PlaceDb]:
        stmt = select(PlaceDb).order_by(PlaceDb.id).offset(offset).limit(limit)
        result = await session.scalars(stmt)
        return result.all()
