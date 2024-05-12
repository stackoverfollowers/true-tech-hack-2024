import logging

from aio_pika.patterns import Master
from aiomisc import Service

from tth.common.places.storage import PlaceStorage
from tth.yolo.recognizer import Recognizer

log = logging.getLogger(__name__)


class YoloService(Service):
    __required__ = ("queue_name",)
    __dependencies__ = ("recognizer", "amqp_master", "place_storage")

    amqp_master: Master
    recognizer: Recognizer
    place_storage: PlaceStorage
    queue_name: str

    async def start(self) -> None:
        await self.amqp_master.create_worker(
            self.queue_name,
            self.process,
            durable=True,
        )
        self.start_event.set()

    async def process(self, *, place_id: int, image_url: str) -> None:
        log.info(
            "Start process task place_id=%s, image_url=%s",
            place_id,
            image_url,
        )
        objs = await self.recognizer.detect_ramp_stair(image_url)
        log.info("Result: %s", objs)
