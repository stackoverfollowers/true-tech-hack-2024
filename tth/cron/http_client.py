import logging

import aiohttp
from pydantic import ValidationError

from tth.common.constants import MTS_DOMAIN, MTS_PLACES_POSTFIX, MTS_REGIONS_POSTFIX
from tth.common.places.models import RegionPlacesMtsModel

log = logging.getLogger(__name__)


class HTTPClient:
    _session: aiohttp.ClientSession

    def __init__(self) -> None:
        self._session = aiohttp.ClientSession(MTS_DOMAIN)

    async def close_session(self) -> None:
        await self._session.close()

    async def get_region_ids(self) -> list[int]:
        async with self._session.get(MTS_REGIONS_POSTFIX) as resp:
            body = await resp.json()

            return [item.get("id") for item in body]

    async def get_places(self,
                         region_id: int,
                         limit: int = 10) -> RegionPlacesMtsModel | None:
        params = {"regionId": region_id,
                  "limit": limit}
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
