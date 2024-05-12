from collections.abc import Mapping, Sequence

import pytest
from aiohttp.test_utils import TestClient, TestServer
from aiohttp.web_app import Application
from aiomisc_log import LogFormat, LogLevel
from fastapi.middleware import Middleware
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from yarl import URL

from tth.common.events.storage import EventStorage
from tth.common.places.storage import PlaceStorage
from tth.common.users.storage import UserStorage
from tth.rest.auth.base import SecurityManager
from tth.rest.middlewares import get_cors_middleware
from tth.rest.service import REST
from tth.rest.users.dispatcher import UserDispatcher


@pytest.fixture
def rest_middlewares() -> Sequence[Middleware]:
    return (get_cors_middleware(),)


@pytest.fixture
def rest_url(localhost: str, aiomisc_unused_port_factory) -> URL:
    return URL.build(
        scheme="http",
        host=localhost,
        port=aiomisc_unused_port_factory(),
    )


@pytest.fixture
def rest_service(
    session_factory: async_sessionmaker[AsyncSession],
    user_storage: UserStorage,
    event_storage: EventStorage,
    place_storage: PlaceStorage,
    security_manager: SecurityManager,
    user_dispatcher: UserDispatcher,
    rest_middlewares: Sequence[Middleware],
    rest_url: URL,
) -> REST:
    return REST(
        address=rest_url.host,
        port=rest_url.port,
        debug=False,
        title="Test Rest",
        description="Test Rest",
        version="test-1.0.0",
        session_factory=session_factory,
        rest_middlewares=rest_middlewares,
        event_storage=event_storage,
        place_storage=place_storage,
        user_storage=user_storage,
        security_manager=security_manager,
        user_dispatcher=user_dispatcher,
    )


@pytest.fixture
def services(rest_service: REST):
    return (rest_service,)


@pytest.fixture
async def api_client(rest_url: URL):
    server = TestServer(Application())
    server._root = rest_url
    client = TestClient(server)
    try:
        yield client
    finally:
        await client.close()


@pytest.fixture
def entrypoint_kwargs() -> Mapping[str, str]:
    return {"log_format": LogFormat.color, "log_level": LogLevel.info}
