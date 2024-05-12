from collections.abc import Sequence

from aio_pika.patterns import Master
from aiomisc_dependency import dependency
from fastapi.middleware import Middleware

from tth.common.args import AMQPGroup, SecurityGroup
from tth.common.events.storage import EventStorage
from tth.common.places.storage import PlaceStorage
from tth.common.users.storage import UserStorage
from tth.cron.parser import MtsPlacesParser
from tth.rest.auth.base import (
    AUTH_COOKIE,
    AUTH_HEADER,
    IAuthProvider,
    SecurityManager,
)
from tth.rest.auth.jwt import JwtAuthProvider, JwtProcessor
from tth.rest.auth.passgen import Passgen
from tth.rest.middlewares import get_cors_middleware
from tth.rest.users.dispatcher import UserDispatcher


def config_deps(security: SecurityGroup, amqp: AMQPGroup) -> None:
    @dependency
    def jwt_processor() -> JwtProcessor:
        return JwtProcessor(
            private_key=security.private_key,
        )

    @dependency
    def auth_provider(jwt_processor: JwtProcessor) -> JwtAuthProvider:
        return JwtAuthProvider(
            jwt_processor=jwt_processor,
            auth_header=AUTH_HEADER,
            auth_cookie=AUTH_COOKIE,
        )

    @dependency
    def security_manager(auth_provider: IAuthProvider) -> SecurityManager:
        return SecurityManager(auth_provider=auth_provider)

    @dependency
    def passgen() -> Passgen:
        return Passgen(secret=security.secret)

    @dependency
    def user_dispatcher(
        user_storage: UserStorage,
        auth_provider: IAuthProvider,
        passgen: Passgen,
    ) -> UserDispatcher:
        return UserDispatcher(
            user_storage=user_storage,
            auth_provider=auth_provider,
            passgen=passgen,
        )

    @dependency
    def cors_middleware() -> Middleware:
        return get_cors_middleware()

    @dependency
    def rest_middlewares(
        cors_middleware: Middleware,
    ) -> Sequence[Middleware]:
        return (cors_middleware,)

    @dependency
    def mts_parser(
        event_storage: EventStorage,
        place_storage: PlaceStorage,
        amqp_master: Master,
    ) -> MtsPlacesParser:
        return MtsPlacesParser(
            event_storage=event_storage,
            place_storage=place_storage,
            amqp_master=amqp_master,
            queue_name=amqp.queue_name,
        )
