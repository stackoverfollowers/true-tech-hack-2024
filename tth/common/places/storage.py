import asyncio
from collections.abc import Iterable, Sequence
from dataclasses import dataclass
from typing import Any

from sqlalchemy import delete, func, select, update
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from tth.common.places.models import (
    CreatePlaceModel,
    PlaceFeatureModel,
    PlaceFromMtsModel,
    PlaceModel,
    PlacePaginationModel,
    PlaceWithFeaturesModel,
    UpdatePlaceModel,
)
from tth.db.models import Feature as FeatureDb
from tth.db.models import FeatureValue
from tth.db.models import Place as PlaceDb
from tth.db.models import PlaceFeature as PlaceFeatureDb
from tth.db.utils import inject_session


@dataclass(frozen=True)
class PlaceStorage:
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
            url=place.url,
            image_url=place.image_url,
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
                address=new_place.address,
                url=new_place.url,
                image_url=new_place.image_url,
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

    @inject_session
    async def save_many_from_mts(
        self,
        places: Iterable[PlaceFromMtsModel],
        session: AsyncSession,
    ) -> Sequence[int]:
        stmt: Any = insert(PlaceDb).values(
            [
                {
                    "id": place_data.id,
                    "name": place_data.title,
                    "address": place_data.address,
                    "url": place_data.url,
                    "image_url": place_data.image_url,
                }
                for place_data in places
            ]
        )

        stmt = stmt.on_conflict_do_update(
            index_elements=[PlaceDb.id],
            set_={
                "name": stmt.excluded.name,
                "address": stmt.excluded.address,
                "url": stmt.excluded.url,
                "image_url": stmt.excluded.image_url,
            },
        ).returning(PlaceDb.id)

        place_ids = await session.scalars(stmt)

        await session.commit()

        return place_ids.all()

    @inject_session
    async def get_many(
        self, session: AsyncSession, place_ids: Sequence[int]
    ) -> Sequence[PlaceModel]:
        query = select(PlaceDb).where(PlaceDb.id.in_(place_ids))
        result = await session.scalars(query)
        return [PlaceModel.model_validate(row) for row in result.all()]

    @inject_session
    async def add_feature(
        self,
        session: AsyncSession,
        place_id: int,
        feature_id: int,
        value: FeatureValue,
    ) -> None:
        stmt = (
            insert(PlaceFeatureDb)
            .values(
                place_id=place_id,
                feature_id=feature_id,
                value=value,
            )
            .returning(PlaceFeatureDb)
        )
        await session.scalars(stmt)
        await session.commit()
