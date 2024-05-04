from collections.abc import Sequence
from datetime import datetime
from typing import Any, Self

from pydantic import BaseModel, ConfigDict

from tth.common.models.pagination import MetaPaginationModel
from tth.db.models import EventType, FeatureValue


class EventModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    place_id: int
    name: str
    event_type: EventType
    url: str
    image_url: str
    description: str
    started_at: datetime
    ended_at: datetime
    created_at: datetime
    updated_at: datetime


class CreateEventModel(BaseModel):
    place_id: int
    name: str
    event_type: EventType
    url: str
    image_url: str
    description: str
    started_at: datetime
    ended_at: datetime


class EventFeatureModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    name: str
    slug: str
    value: FeatureValue


class EventWithFeaturesModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    place_id: int
    name: str
    event_type: EventType
    url: str
    image_url: str
    description: str
    started_at: datetime
    ended_at: datetime
    created_at: datetime
    updated_at: datetime

    features: Sequence[FeatureValue]


class EventPaginationModel(BaseModel):
    meta: MetaPaginationModel
    items: Sequence[EventModel]

    @classmethod
    def build(
        cls,
        limit: int,
        offset: int,
        total: int,
        items: Sequence[Any],
    ) -> Self:
        return cls(
            meta=MetaPaginationModel(limit=limit, offset=offset, total=total),
            items=[EventModel.model_validate(item) for item in items],
        )


class UpdateEventModel(BaseModel):
    name: str | None = None
    description: str | None = None
    event_type: EventType | None = None
    url: str | None = None
    image_url: str | None = None
    started_at: datetime | None = None
    ended_at: datetime | None = None
