import abc

from tth.common.events.models import Event


class IEventStorage(abc.ABC):
    async def get_by_id(self, event_id: int) -> Event | None:
        raise NotImplementedError
