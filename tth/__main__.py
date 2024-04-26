import logging

from aiomisc import Service, entrypoint
from aiomisc_log import basic_config

from tth.args import Parser
from tth.bot.service import TelegramBotService
from tth.deps import config_deps
from tth.rest.service import REST

log = logging.getLogger(__name__)


def main() -> None:
    parser = Parser(auto_env_var_prefix="APP_")
    parser.parse_args([])
    parser.sanitize_env()
    config_deps(parser)
    basic_config(level=parser.log.level, log_format=parser.log.format)

    services: list[Service] = [
        REST(
            host=parser.http.host,
            port=parser.http.port,
            debug=parser.debug,
            title=parser.project.title,
            description=parser.project.description,
            version=parser.project.version,
        ),
        TelegramBotService(),
    ]

    with entrypoint(
        *services,
        log_level=parser.log.level,
        log_format=parser.log.format,
        pool_size=parser.pool_size,
        debug=parser.debug,
    ) as loop:
        log.info(
            "REST service started on address %s:%s",
            parser.http.host,
            parser.http.port,
        )
        loop.run_forever()


if __name__ == "__main__":
    main()
