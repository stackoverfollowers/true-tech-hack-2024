import logging
from collections.abc import AsyncGenerator, AsyncIterator

import aio_pika
from aio_pika.abc import AbstractConnection
from aio_pika.patterns import Master
from aiomisc_dependency import dependency
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker

from tth.common.args import AMQPGroup, DatabaseGroup
from tth.common.events.storage import EventStorage
from tth.common.places.storage import PlaceStorage
from tth.common.users.storage import UserStorage
from tth.db.utils import (
    create_async_engine,
    create_async_session_factory,
)

log = logging.getLogger(__name__)


def config_deps(db: DatabaseGroup, debug: bool, amqp: AMQPGroup) -> None:
    @dependency
    async def engine() -> AsyncGenerator[AsyncEngine, None]:
        engine = create_async_engine(
            connection_uri=str(db.pg_dsn),
            echo=debug,
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
    ) -> EventStorage:
        return EventStorage(session_factory=session_factory)

    @dependency
    def place_storage(
        session_factory: async_sessionmaker[AsyncSession],
    ) -> PlaceStorage:
        return PlaceStorage(session_factory=session_factory)

    @dependency
    async def amqp_conn() -> AsyncIterator[AbstractConnection]:
        log.info("Starting AMQP robust connection")
        amqp_conn = await aio_pika.connect_robust(
            str(amqp.dsn),
            client_properties={
                "connection_name": "tth",
            },
        )
        async with amqp_conn:
            yield amqp_conn
        log.info("AMQP connection was closed")

    @dependency
    async def amqp_master(amqp_conn: AbstractConnection) -> AsyncIterator[Master]:
        async with amqp_conn.channel() as channel:
            await channel.set_qos(prefetch_count=amqp.prefetch_count)
            log.info(
                "RabbitMQ channel for recognizer created with prefetch count %s",
                amqp.prefetch_count,
            )
            yield Master(channel)
