from dataclasses import dataclass
from datetime import datetime
from typing import Self

from tth.db.models import Event as EventDb


@dataclass(frozen=True)
class Event:
    id: int
    place_id: int
    name: str
    description: str
    started_at: datetime
    ended_at: datetime

    @classmethod
    def build(cls, obj: EventDb) -> Self:
        return cls(
            id=obj.id,
            place_id=obj.place_id,
            name=obj.name,
            description=obj.description,
            started_at=obj.started_at,
            ended_at=obj.ended_at,
        )
