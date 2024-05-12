import argclass

from tth.common.args import (
    AMQPGroup,
    DatabaseGroup,
    LogGroup,
    YoloGroup,
)


class YoloParser(argclass.Parser):
    debug: bool = argclass.Argument(
        "-D",
        "--debug",
        default=False,
        type=lambda x: x.lower() == "true",
    )
    pool_size: int = argclass.Argument(
        "-s", "--pool-size", type=int, default=4, help="Thread pool size"
    )

    log = LogGroup(title="Logging options")
    db = DatabaseGroup(title="Database options")
    yolo = YoloGroup(title="Yolo options")
    amqp = AMQPGroup(title="AMQP options")
