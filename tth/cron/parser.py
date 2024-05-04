import asyncio
import itertools
import logging
from collections.abc import Iterable, Sequence
from dataclasses import dataclass

from tth.common.events.storage import IEventStorage
from tth.common.places.models import PlaceFromMtsModel
from tth.common.places.storage import IPlaceStorage
from tth.cron.http_client import HTTPClient

log = logging.getLogger(__name__)


@dataclass(frozen=True)
class MtsPlacesParser:
    event_storage: IEventStorage
    place_storage: IPlaceStorage

    async def parse(self) -> None:
        client = HTTPClient()
        region_ids = await client.get_region_ids()

        await self.place_storage.save_many_from_mts(
            *await asyncio.gather(
                self._get_places(client=client,
                                 region_ids=region_ids)
            )
        )

        await client.close_session()

    async def _get_places(
        self,
        client: HTTPClient,
        region_ids: Sequence[int],
    ) -> Iterable[PlaceFromMtsModel]:
        tasks = [
            self._get_region_places(client, region_id)
            for region_id in region_ids
        ]
        results = await asyncio.gather(*tasks)

        return itertools.chain(*results)

    @staticmethod
    async def _get_region_places(
        client: HTTPClient,
        region_id: int,
    ) -> Sequence[PlaceFromMtsModel]:
        some_places = await client.get_places(region_id)
        if some_places is None:
            return []

        all_places = await client.get_places(
            region_id=region_id,
            limit=some_places.total)
        return [] if all_places is None else all_places.items
