import logging
from asyncio import Lock
from collections.abc import Sequence
from dataclasses import dataclass
from enum import StrEnum

from aiomisc import threaded
from ultralytics import YOLO

log = logging.getLogger(__name__)


class RecognizedFeatures(StrEnum):
    RAMP = "RAMP"
    STAIRS = "STAIRS"


@dataclass(frozen=True)
class Recognizer:
    yolo_model: YOLO
    yolo_lock: Lock
    image_size: int
    conf: float

    async def recognize(self, image_url: str) -> Sequence[RecognizedFeatures]:
        detected: Sequence[RecognizedFeatures] = []
        async with self.yolo_lock:
            try:
                detected = await self.detect_ramp_stair(image_url=image_url)
            except Exception as e:  # noqa: BLE001
                log.warning("Exception occured", stack_info=True, exc_info=e)
        return detected

    @threaded
    def detect_ramp_stair(self, image_url: str) -> Sequence[RecognizedFeatures]:
        result = self.yolo_model.predict(image_url, save=False, imgsz=640, conf=0.5)[0]
        detected_objects = []
        for box in result.boxes:
            for b in box:
                for t in b.cls:
                    val: str | None = result.names.get(int(t))
                    if val is not None:
                        detected_objects.append(RecognizedFeatures(val.upper()))

        return detected_objects
