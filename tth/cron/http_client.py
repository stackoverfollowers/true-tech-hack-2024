import asyncio
import logging

import aiohttp
from pydantic import ValidationError

from tth.common.constants import (
    MTS_DOMAIN,
    MTS_EVENTS_POSTFIX,
    MTS_PLACES_POSTFIX,
    MTS_REGIONS_POSTFIX,
)
from tth.common.events.models import RegionEventsMtsModel
from tth.common.places.models import RegionPlacesMtsModel
from tth.db.models import EventType

log = logging.getLogger(__name__)


class HTTPClient:
    _session: aiohttp.ClientSession

    def __init__(self) -> None:
        connector = aiohttp.TCPConnector(limit=10)
        self._session = aiohttp.ClientSession(MTS_DOMAIN, connector=connector, )
        self.sem = asyncio.Semaphore(value=20)

    async def init_session(self) -> None:
        async with self.sem:
            await self._session.get("/")

    async def close_session(self) -> None:
        async with self.sem:
            await self._session.close()

    async def get_region_ids(self) -> list[int]:

        async with self.sem:
            async with self._session.get(MTS_REGIONS_POSTFIX) as resp:
                body = await resp.json()

                return [item.get("id") for item in body]

    async def get_places(self,
                         region_id: int,
                         limit: int = 10) -> RegionPlacesMtsModel | None:
        params = {"regionId": region_id,
                  "limit": limit}

        async with self.sem:
            async with self._session.get(MTS_PLACES_POSTFIX,
                                         params=params) as resp:
                if not resp.ok:
                    log.info(
                        "Failed to get places for region %s. "
                        "Response status: %s",
                        region_id,
                        resp.status,
                    )
                    return None
                body = await resp.read()
            try:
                return RegionPlacesMtsModel.model_validate_json(body)
            except ValidationError:
                log.exception(
                    "Parsing is failed. Region ID: %s Body: %s",
                    region_id, body,
                )
                return None

    async def get_events_by_type(
        self,
        region_id: int,
        event_type: EventType,
        offset: int = 0,
        limit: int = 10,
    ) -> RegionEventsMtsModel | None:
        params = {"regionId": region_id, "limit": limit, "offset": offset}

        async with self.sem:
            async with self._session.get(MTS_EVENTS_POSTFIX + event_type,
                                         params=params) as resp:
                if not resp.ok:
                    log.info(
                        "Failed to get events: URL: %s. "
                        "Response status: %s",
                        resp.url,
                        resp.status,
                    )
                    return None
                body = await resp.read()
            try:
                return RegionEventsMtsModel.model_validate_json(body)
            except ValidationError:
                log.exception(
                    "Parsing is failed. Region ID: %s Body: %s",
                    region_id, body,
                )
            return None
