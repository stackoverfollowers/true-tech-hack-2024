from collections.abc import Sequence
from datetime import datetime
from typing import Any, Self

from pydantic import BaseModel, ConfigDict

from tth.common.models.pagination import MetaPaginationModel
from tth.db.models import FeatureValue


class PlaceModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    description: str
    address: str
    created_at: datetime
    updated_at: datetime


class CreatePlaceModel(BaseModel):
    name: str
    description: str
    address: str


class PlaceFeatureModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    name: str
    slug: str
    value: FeatureValue


class PlaceWithFeaturesModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    description: str
    address: str
    created_at: datetime
    updated_at: datetime

    features: Sequence[FeatureValue]


class PlacePaginationModel(BaseModel):
    meta: MetaPaginationModel
    items: Sequence[PlaceModel]

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
            items=[PlaceModel.model_validate(item) for item in items],
        )


class UpdatePlaceModel(BaseModel):
    name: str | None = None
    description: str | None = None
    address: str | None = None
