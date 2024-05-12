from dataclasses import dataclass

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from tth.common.features.models import FeatureModel
from tth.db.models import Feature as FeatureDb
from tth.db.utils import inject_session


@dataclass(frozen=True)
class FeatureStorage:
    session_factory: async_sessionmaker[AsyncSession]

    @inject_session
    async def get_by_slug(
        self,
        session: AsyncSession,
        slug: str,
    ) -> FeatureModel | None:
        stmt = select(FeatureDb).where(FeatureDb.slug == slug)
        obj = (await session.scalars(stmt)).first()
        return FeatureModel.model_validate(obj) if obj else None
