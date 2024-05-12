from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException, Query, Response

from tth.common.places.models import (
    CreatePlaceModel,
    PlaceModel,
    PlacePaginationModel,
    PlaceWithFeaturesModel,
    UpdatePlaceModel,
)
from tth.common.places.storage import IPlaceStorage
from tth.rest.overrides import GetPlaceStorage

router = APIRouter(prefix="/places", tags=["Places"])

@router.get("", response_model=PlacePaginationModel)
async def get_places(
    limit: int = Query(default=20, gt=0, le=100),
    offset: int = Query(default=0, gt=-1),
    place_storage: IPlaceStorage = Depends(GetPlaceStorage),
) -> PlacePaginationModel:
    return await place_storage.pagination(limit=limit, offset=offset)


@router.post("", response_model=PlaceModel)
async def create_place(
    new_place: CreatePlaceModel,
    place_storage: IPlaceStorage = Depends(GetPlaceStorage),
) -> PlaceModel:
    return await place_storage.create(
        new_place=new_place,
    )


@router.get(
    "/{place_id}",
    response_model=PlaceWithFeaturesModel,
    summary="Get Place with features",
)
async def get_place(
    place_id: int,
    place_storage: IPlaceStorage = Depends(GetPlaceStorage),
) -> PlaceWithFeaturesModel:
    place = await place_storage.get_by_id_with_features(place_id=place_id)
    if place is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail="Place not found",
        )
    return place


@router.post("/{place_id}")
async def update_place(
    place_id: int,
    update_place: UpdatePlaceModel,
    place_storage: IPlaceStorage = Depends(GetPlaceStorage),
) -> PlaceModel:
    return await place_storage.update(
        place_id=place_id,
        update_place=update_place,
    )


@router.delete("/{place_id}", status_code=204)
async def delete_place(
    place_id: int,
    response: Response,
    place_storage: IPlaceStorage = Depends(GetPlaceStorage),
) -> Response:
    await place_storage.delete(place_id=place_id)
    response.status_code = HTTPStatus.NO_CONTENT
    return response
