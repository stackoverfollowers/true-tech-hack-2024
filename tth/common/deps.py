from collections.abc import AsyncGenerator

from aiomisc_dependency import dependency
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker

from tth.args import Parser
from tth.common.events.storage import EventStorage, IEventStorage
from tth.common.places.storage import IPlaceStorage, PlaceStorage
from tth.common.users.storage import UserStorage
from tth.db.utils import (
    create_async_engine,
    create_async_session_factory,
)


def config_deps(parser: Parser) -> None:
    @dependency
    async def engine() -> AsyncGenerator[AsyncEngine, None]:
        engine = create_async_engine(
            connection_uri=str(parser.db.pg_dsn),
            echo=parser.debug,
            pool_pre_ping=True,
        )
        yield engine
        await engine.dispose()

    @dependency
    def session_factory(
        engine: AsyncEngine,
    ) -> async_sessionmaker[AsyncSession]:
        return create_async_session_factory(engine=engine)

    @dependency
    def user_storage(
        session_factory: async_sessionmaker[AsyncSession],
    ) -> UserStorage:
        return UserStorage(session_factory=session_factory)

    @dependency
    def event_storage(
        session_factory: async_sessionmaker[AsyncSession],
    ) -> IEventStorage:
        return EventStorage(session_factory=session_factory)

    @dependency
    def place_storage(
        session_factory: async_sessionmaker[AsyncSession],
    ) -> IPlaceStorage:
        return PlaceStorage(session_factory=session_factory)
