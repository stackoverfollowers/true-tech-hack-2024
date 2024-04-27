from dataclasses import dataclass
from typing import Self

from tth.db.models import Disability as DisabilityDb
from tth.db.models import DisabilityStatus


@dataclass(frozen=True)
class Disability:
    name: str
    group: str
    status: DisabilityStatus

    @classmethod
    def build(cls, obj: DisabilityDb) -> Self:
        return cls(
            name=obj.name,
            group=obj.group,
            status=obj.status,
        )
