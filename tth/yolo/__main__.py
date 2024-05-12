import logging

from aiomisc import Service, entrypoint
from aiomisc_log import basic_config

from tth.common.deps import config_deps as config_common_deps
from tth.yolo.args import YoloParser
from tth.yolo.deps import config_yolo_deps
from tth.yolo.service import YoloService

log = logging.getLogger(__name__)


def main() -> None:
    parser = YoloParser(auto_env_var_prefix="APP_")
    parser.parse_args([])
    parser.sanitize_env()
    config_common_deps(
        db=parser.db,
        debug=parser.debug,
        amqp=parser.amqp,
    )
    config_yolo_deps(yolo=parser.yolo)
    basic_config(level=parser.log.level, log_format=parser.log.format)

    services: list[Service] = [
        YoloService(queue_name=parser.amqp.queue_name),
    ]

    with entrypoint(
        *services,
        log_level=parser.log.level,
        log_format=parser.log.format,
        pool_size=parser.pool_size,
        debug=parser.debug,
    ) as loop:
        log.info("Start YOLO service")
        loop.run_forever()


if __name__ == "__main__":
    main()
