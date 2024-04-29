from collections.abc import Callable, Sequence

from aiomisc.service.uvicorn import UvicornApplication, UvicornService
from fastapi import FastAPI, HTTPException
from sqlalchemy.exc import DBAPIError
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from starlette.middleware import Middleware

from tth.common.events.storage import IEventStorage
from tth.common.exceptions import (
    HackTemplateException,
    UserWithUsernameAlreadyExistsException,
)
from tth.common.users.storage import UserStorage
from tth.rest.api.router import router as api_router
from tth.rest.auth.base import SecurityManager
from tth.rest.exception_handlers import (
    db_api_error_handler,
    http_exception_handler,
    internal_server_error_handler,
    user_already_exists_handler,
)
from tth.rest.overrides import (
    MAYBE_AUTH,
    REQUIRE_ADMIN_AUTH,
    REQUIRE_AUTH,
    REQUIRE_REGULAR_AUTH,
    GetEventStorage,
    GetSessionFactory,
    GetUserDispatcher,
    GetUserStorage,
)
from tth.rest.users.dispatcher import UserDispatcher

ExceptionHandlersType = tuple[tuple[type[Exception], Callable], ...]


class REST(UvicornService):
    __required__ = (
        "debug",
        "title",
        "description",
        "version",
    )
    __dependencies__ = (
        "session_factory",
        "rest_middlewares",
        "user_storage",
        "security_manager",
        "user_dispatcher",
        "event_storage",
    )

    EXCEPTION_HANDLERS: ExceptionHandlersType = (
        (HTTPException, http_exception_handler),
        (UserWithUsernameAlreadyExistsException, user_already_exists_handler),
        (HackTemplateException, internal_server_error_handler),
        (DBAPIError, db_api_error_handler),
    )

    debug: bool
    title: str
    description: str
    version: str

    session_factory: async_sessionmaker[AsyncSession]
    security_manager: SecurityManager
    rest_middlewares: Sequence[Middleware]
    user_storage: UserStorage
    user_dispatcher: UserDispatcher
    event_storage: IEventStorage

    async def create_application(self) -> UvicornApplication:
        app = FastAPI(
            debug=self.debug,
            title=self.title,
            description=self.description,
            version=self.version,
            openapi_url="/docs/openapi.json",
            docs_url="/docs/swagger",
            redoc_url="/docs/redoc",
        )
        self._add_middlewares(app)
        self._add_routes(app)
        self._add_exceptions(app)
        self._add_dependency_overrides(app)
        return app

    def _add_middlewares(self, app: FastAPI) -> None:
        for middleware in self.rest_middlewares[::-1]:
            app.user_middleware.append(middleware)

    def _add_routes(self, app: FastAPI) -> None:
        app.include_router(api_router)

    def _add_exceptions(self, app: FastAPI) -> None:
        for exception, handler in self.EXCEPTION_HANDLERS:
            app.add_exception_handler(exception, handler)

    def _add_dependency_overrides(self, app: FastAPI) -> None:
        app.dependency_overrides.update(
            {
                MAYBE_AUTH: self.security_manager.maybe_auth,
                REQUIRE_AUTH: self.security_manager.require_auth,
                REQUIRE_ADMIN_AUTH: self.security_manager.require_admin_auth,
                REQUIRE_REGULAR_AUTH: self.security_manager.require_regular_auth,
                GetSessionFactory: lambda: self.session_factory,
                GetUserStorage: lambda: self.user_storage,
                GetUserDispatcher: lambda: self.user_dispatcher,
                GetEventStorage: lambda: self.event_storage,
            }
        )
