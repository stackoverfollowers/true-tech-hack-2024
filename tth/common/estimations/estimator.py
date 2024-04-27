from collections import defaultdict
from collections.abc import Mapping, Sequence
from itertools import chain

from tth.common.disabilities.models import Disability
from tth.common.disabilities.storage import IDisabilityStorage
from tth.common.events.storage import IEventStorage


class Estimator:
    _disability_storage: IDisabilityStorage
    _event_storage: IEventStorage

    def __init__(
        self,
        event_storage: IEventStorage,
        disability_storage: IDisabilityStorage,
    ) -> None:
        self._disability_storage = disability_storage
        self._event_storage = event_storage

    async def estimate(self, user_id: int, event_id: int) -> Mapping[str, int]:
        event = await self._event_storage.get_by_id(event_id)
        if event is None:
            return {}
        user_disabilities = await self._disability_storage.get_user_disabilities(
            user_id
        )
        event_disabilities = await self._disability_storage.get_full_event_disabilities(
            event_id=event_id, place_id=event.place_id
        )
        grouped_user_disabilities = grouped_disabilities(user_disabilities)
        grouped_event_disabilities = grouped_disabilities(event_disabilities)
        result: dict[str, int] = {}
        for k, v in chain(
            grouped_user_disabilities.items(),
            grouped_event_disabilities.items(),
        ):
            result[k] = result.get(k, 0) + v

        return result


def grouped_disabilities(disabilities: Sequence[Disability]) -> Mapping[str, int]:
    grouped: dict[str, int] = defaultdict(int)
    for disability in disabilities:
        grouped[disability.group] += disability.status
    return grouped
