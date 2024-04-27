from collections.abc import Sequence

import ujson
from aiogram import BaseMiddleware, Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.fsm.storage.base import BaseStorage
from aiogram.fsm.storage.memory import MemoryStorage, SimpleEventIsolation
from aiogram.fsm.storage.redis import DefaultKeyBuilder, RedisStorage
from aiomisc_dependency import dependency
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from tth.args import Parser
from tth.bot.middlewares.deps import DepsMiddleware
from tth.bot.middlewares.user import UserMiddleware
from tth.common.telegram.storage import TelegramStorage
from tth.common.users.storage import UserStorage


def config_deps(parser: Parser) -> None:
    @dependency
    def bot() -> Bot:
        return Bot(
            token=parser.telegram.bot_token,
            parse_mode=ParseMode.HTML,
        )

    @dependency
    def fsm_storage() -> BaseStorage:
        if parser.debug:
            return MemoryStorage()
        return RedisStorage.from_url(
            url=str(parser.redis.redis_dsn),
            key_builder=DefaultKeyBuilder(with_destiny=True),
            json_loads=ujson.loads,
            json_dumps=ujson.dumps,
        )

    @dependency
    def dispatcher(
        fsm_storage: BaseStorage,
    ) -> Dispatcher:
        return Dispatcher(
            storage=fsm_storage,
            events_isolation=SimpleEventIsolation(),
        )

    @dependency
    def telegram_storage(
        session_factory: async_sessionmaker[AsyncSession],
    ) -> TelegramStorage:
        return TelegramStorage(
            session_factory=session_factory,
        )

    @dependency
    def user_middleware(telegram_storage: TelegramStorage) -> BaseMiddleware:
        return UserMiddleware(telegram_storage=telegram_storage)

    @dependency
    def deps_middleware(
        user_storage: UserStorage,
        telegram_storage: TelegramStorage,
    ) -> BaseMiddleware:
        return DepsMiddleware(
            deps={
                "user_storage": user_storage,
                "telegram_storage": telegram_storage,
            },
        )

    @dependency
    def bot_middlewares(
        user_middleware: BaseMiddleware,
        deps_middleware: BaseMiddleware,
    ) -> Sequence[BaseMiddleware]:
        return (user_middleware, deps_middleware)
