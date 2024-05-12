from base64 import b64decode
from pathlib import Path

import argclass
from aiomisc_log import LogFormat, LogLevel
from yarl import URL


def load_base64(value: str) -> str:
    return b64decode(value).decode()


class SecurityGroup(argclass.Group):
    secret: str = argclass.Secret(
        "--secret", type=str, required=True, help="Secret key"
    )
    private_key: str = argclass.Secret(
        "--private-key", type=load_base64, required=True, help="Private key"
    )


class LogGroup(argclass.Group):
    level: LogLevel = argclass.EnumArgument(LogLevel, default=LogLevel.info)
    format: LogFormat = argclass.EnumArgument(LogFormat, default=LogFormat.color)


class HostPortGroup(argclass.Group):
    host: str = argclass.Argument("--host", type=str, default="127.0.0.1")
    port: int = argclass.Argument("--port", type=int, default=8000)


class ProjectGroup(argclass.Group):
    title: str = argclass.Argument(
        "--title",
        type=str,
        default="REST service",
        help="Project title",
    )
    description = argclass.Argument(
        "--description",
        type=str,
        default="REST service",
        help="Project description",
    )
    version = argclass.Argument(
        "--version",
        type=str,
        default="1.0.0",
        help="Project version",
    )


class DatabaseGroup(argclass.Group):
    pg_dsn: URL = argclass.Argument("--pg-dsn", required=True, type=URL)


class AMQPGroup(argclass.Group):
    dsn: URL = argclass.Argument(type=URL, required=True)
    prefetch_count: int = argclass.Argument(type=int, default=4)
    retry_pause_seconds: int = argclass.Argument(type=int, default=60)
    retry_count_limit: int = argclass.Argument(type=int, default=2)
    queue_name: str = argclass.Argument(type=str, default="yolo_queue")


class YoloGroup(argclass.Group):
    model_path: Path = argclass.Argument(type=Path, required=True)
    image_size: int = argclass.Argument(type=int, default=640)
    conf: float = argclass.Argument(type=float, default=0.5)


class ParserGroup(argclass.Group):
    cron_spec: str = argclass.Argument(type=str, default="*/43 * * * *")
