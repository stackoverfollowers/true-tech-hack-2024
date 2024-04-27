from collections.abc import AsyncGenerator

from aiomisc_dependency import dependency
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker

from tth.args import Parser
from tth.common.disabilities.storage import (
    DisabilityCachedStorage,
    DisabilityStorage,
    IDisabilityStorage,
)
from tth.common.estimations.estimator import Estimator
from tth.common.events.storage import IEventStorage
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
    def disability_storage(
        session_factory: async_sessionmaker[AsyncSession],
    ) -> IDisabilityStorage:
        storage = DisabilityStorage(session_factory=session_factory)
        if parser.with_cache:
            return DisabilityCachedStorage(storage=storage)
        return storage

    @dependency
    def event_storage(
        session_factory: async_sessionmaker[AsyncSession],
    ) -> IEventStorage:
        pass

    @dependency
    def estimator(
        disability_storage: IDisabilityStorage,
        event_storage: IEventStorage,
    ) -> Estimator:
        return Estimator(
            disability_storage=disability_storage, event_storage=event_storage
        )
