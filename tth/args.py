import argclass

from tth.common.args import (
    AMQPGroup,
    DatabaseGroup,
    HostPortGroup,
    LogGroup,
    ParserGroup,
    ProjectGroup,
    SecurityGroup,
)


class Parser(argclass.Parser):
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
    http = HostPortGroup(title="HTTP options")
    project = ProjectGroup(title="Project options")
    db = DatabaseGroup(title="Database options")
    security = SecurityGroup(title="Security options")
    amqp = AMQPGroup(title="AMQP options")
    parser = ParserGroup(title="Parser options")
