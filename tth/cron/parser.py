import asyncio
import itertools
import logging
from collections.abc import Iterable, Sequence
from dataclasses import dataclass

from tth.common.events.models import EventFromMtsModel
from tth.common.events.storage import IEventStorage
from tth.common.places.models import PlaceFromMtsModel
from tth.common.places.storage import IPlaceStorage
from tth.cron.http_client import HTTPClient
from tth.db.models import EventType

log = logging.getLogger(__name__)

CHUNK_SIZE = 100


@dataclass(frozen=True)
class MtsPlacesParser:
    event_storage: IEventStorage
    place_storage: IPlaceStorage

    async def parse(self) -> None:
        client = HTTPClient()

        region_ids = await client.get_region_ids()

        place_ids = set(await self.place_storage.save_many_from_mts(
            places=await self._get_places(client=client,
                                          region_ids=region_ids)
        ))
        log.info("Got %s places", len(place_ids))

        await client.init_session()

        events = await self._get_events(
            client=client,
            region_ids=region_ids)

        event_ids = await self.event_storage.save_many_from_mts(
            events=self.filter_events_by_places(events, place_ids)
        )
        log.info("Got %s events", len(event_ids))
        await client.close_session()

    @staticmethod
    def filter_events_by_places(
        events: Iterable[EventFromMtsModel],
        place_ids: set[int],
    ) -> Iterable[EventFromMtsModel]:
        """Filter unique events with existing venue"""
        event_ids = set()
        for event in events:
            if event.venue.id in place_ids:
                if event.id not in event_ids:
                    yield event
                    event_ids.add(event.id)

    async def _get_places(
        self,
        client: HTTPClient,
        region_ids: Sequence[int],
    ) -> Iterable[PlaceFromMtsModel]:
        tasks = [
            self._get_region_places(client=client, region_id=region_id)
            for region_id in region_ids
        ]
        results = await asyncio.gather(*tasks)

        return itertools.chain(*results)

    @staticmethod
    async def _get_region_places(
        client: HTTPClient,
        region_id: int,
    ) -> Sequence[PlaceFromMtsModel]:
        some_places = await client.get_places(region_id=region_id)
        if some_places is None:
            return []

        all_places = await client.get_places(
            region_id=region_id,
            limit=some_places.total)
        return [] if all_places is None else all_places.items

    async def _get_events(
        self,
        client: HTTPClient,
        region_ids: Sequence[int],
    ) -> Iterable[EventFromMtsModel]:

        results = await asyncio.gather(*[
            self._get_region_events(
                client=client,
                region_id=region_id,
            )
            for region_id in region_ids
        ])

        return itertools.chain(*results)

    async def _get_region_events(
        self,
        client: HTTPClient,
        region_id: int,
    ) -> Iterable[EventFromMtsModel]:

        results = await asyncio.gather(*[
            self._get_all_region_events_by_type(
                client=client,
                region_id=region_id,
                event_type=event_type)
            for event_type in EventType
        ])

        return itertools.chain(*results)

    @staticmethod
    async def _get_all_region_events_by_type(
        client: HTTPClient,
        region_id: int,
        event_type: EventType,
    ) -> Iterable[EventFromMtsModel]:

        some_events = await client.get_events_by_type(
            region_id=region_id,
            event_type=event_type)
        if some_events is None:
            return []

        total = some_events.total
        offset, limit = 0, CHUNK_SIZE
        tasks = [
            client.get_events_by_type(
                region_id=region_id,
                event_type=event_type,
                offset=offset,
                limit=limit
            )
        ]

        while (offset + limit) <= total:
            offset += limit
            tasks.append(client.get_events_by_type(
                region_id=region_id,
                event_type=event_type,
                offset=offset,
                limit=limit
            ))

        results = await asyncio.gather(*tasks)

        def add_event_type(
            items: Sequence[EventFromMtsModel]
        ) -> Sequence[EventFromMtsModel]:
            for item in items:
                item.event_type = event_type
            return items

        return itertools.chain(*[
            add_event_type(res.items)
            for res in results
            if res is not None]
        )
