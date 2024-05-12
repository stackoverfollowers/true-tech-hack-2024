from asyncio import Lock

from aiomisc_dependency import dependency
from ultralytics import YOLO

from tth.common.args import YoloGroup
from tth.yolo.recognizer import Recognizer


def config_yolo_deps(yolo: YoloGroup) -> None:
    @dependency
    def yolo_model() -> YOLO:
        return YOLO(model=yolo.model_path)

    @dependency
    def recognizer(yolo_model: YOLO) -> Recognizer:
        return Recognizer(
            yolo_model=yolo_model,
            yolo_lock=Lock(),
            image_size=yolo.image_size,
            conf=yolo.conf,
        )
