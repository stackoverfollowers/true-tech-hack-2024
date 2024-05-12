from collections.abc import Sequence
from datetime import datetime
from typing import Any, Self

from pydantic import BaseModel, ConfigDict, Field

from tth.common.constants import MTS_DOMAIN
from tth.common.models.pagination import MetaPaginationModel
from tth.db.models import FeatureValue


class PlaceModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    url: str
    image_url: str
    description: str | None
    address: str
    created_at: datetime
    updated_at: datetime


class CreatePlaceModel(BaseModel):
    name: str
    url: str
    image_url: str
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
    url: str
    image_url: str
    description: str | None
    address: str
    created_at: datetime
    updated_at: datetime

    features: Sequence[PlaceFeatureModel]


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
    url: str | None = None
    image_url: str | None = None


class PlaceFromMtsModel(BaseModel):
    id: int
    title: str
    address: str
    url: str
    image_url: str = Field(alias="imageUrl")

    def model_post_init(self, __context: Any) -> None:
        if not self.url.startswith(MTS_DOMAIN):
            self.url = MTS_DOMAIN + self.url

        if not self.image_url.startswith(MTS_DOMAIN):
            self.image_url = MTS_DOMAIN + self.image_url


class PlaceInEventFromMtsModel(BaseModel):
    id: int
    title: str
    url: str


class RegionPlacesMtsModel(BaseModel):
    total: int
    items: Sequence[PlaceFromMtsModel]
