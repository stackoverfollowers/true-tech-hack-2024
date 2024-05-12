import logging
import os
from asyncio import Lock
from dataclasses import dataclass
from enum import StrEnum

from aiomisc import threaded
from ultralytics import YOLO

log = logging.getLogger(__name__)


class RecognizedFeatureSlugs(StrEnum):
    RAMP = "ramp"
    STAIRS = "stairs"


@dataclass(frozen=True)
class Recognizer:
    yolo_model: YOLO
    yolo_lock: Lock
    image_size: int
    conf: float

    async def recognize(self, image_url: str) -> set[RecognizedFeatureSlugs]:
        detected: set[RecognizedFeatureSlugs] = set()
        async with self.yolo_lock:
            try:
                detected = await self._detect_ramp_stair(image_url=image_url)
            except Exception as e:  # noqa: BLE001
                log.warning("Exception occured", stack_info=True, exc_info=e)
            await self._remove_file(image_url)
        return detected

    @threaded
    def _detect_ramp_stair(self, image_url: str) -> set[RecognizedFeatureSlugs]:
        result = self.yolo_model.predict(
            image_url,
            save=False,
            imgsz=640,
            conf=0.5,
            save_dir="/tmp",
        )[0]
        detected_objects = set()
        for box in result.boxes:
            for b in box:
                for t in b.cls:
                    val: str | None = result.names.get(int(t))
                    if val is not None:
                        detected_objects.add(RecognizedFeatureSlugs(val))

        return detected_objects

    @threaded
    def _remove_file(self, image_url: str) -> None:
        file = image_url.rsplit("/", 1)[1]
        try:
            os.remove(file)
        except OSError:
            pass
