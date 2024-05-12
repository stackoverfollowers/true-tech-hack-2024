import logging

from aio_pika.patterns import Master
from aiomisc import Service

from tth.common.features.storage import FeatureStorage
from tth.common.places.storage import PlaceStorage
from tth.db.models import FeatureValue
from tth.yolo.recognizer import Recognizer

log = logging.getLogger(__name__)


class YoloService(Service):
    __required__ = ("queue_name",)
    __dependencies__ = (
        "recognizer",
        "amqp_master",
        "place_storage",
        "feature_storage",
    )

    amqp_master: Master
    recognizer: Recognizer
    feature_storage: FeatureStorage
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
        recognized_features = await self.recognizer.recognize(image_url)
        log.info("Result: %s", recognized_features)
        for feature_slug in recognized_features:
            feature = await self.feature_storage.get_by_slug(slug=feature_slug)
            if feature is None:
                continue
            await self.place_storage.add_feature(
                place_id=place_id,
                feature_id=feature.id,
                value=FeatureValue.AVAILABLE,
            )
