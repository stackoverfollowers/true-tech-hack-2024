from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException, Query, Response

from tth.common.events.models import (
    CreateEventModel,
    EventModel,
    EventPaginationModel,
    EventWithFeaturesModel,
    UpdateEventModel,
)
from tth.common.events.storage import IEventStorage
from tth.rest.overrides import GetEventStorage

router = APIRouter(prefix="/events", tags=["Events"])


@router.get("", response_model=EventPaginationModel)
async def get_events(
    limit: int = Query(default=20, gt=0, le=100),
    offset: int = Query(default=0, gt=-1),
    event_storage: IEventStorage = Depends(GetEventStorage),
) -> EventPaginationModel:
    return await event_storage.pagination(limit=limit, offset=offset)


@router.post("", response_model=EventModel)
async def create_event(
    new_event: CreateEventModel,
    event_storage: IEventStorage = Depends(GetEventStorage),
) -> EventModel:
    return await event_storage.create(
        place_id=new_event.place_id,
        name=new_event.name,
        description=new_event.description,
        started_at=new_event.started_at,
        ended_at=new_event.ended_at,
    )


@router.get(
    "/{event_id}",
    response_model=EventWithFeaturesModel,
    summary="Get Event with features",
)
async def get_event(
    event_id: int,
    event_storage: IEventStorage = Depends(GetEventStorage),
) -> EventWithFeaturesModel:
    event = await event_storage.get_by_id_with_features(event_id=event_id)
    if event is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail="Event not found",
        )
    return event


@router.post("/{event_id}")
async def update_event(
    event_id: int,
    update_event: UpdateEventModel,
    event_storage: IEventStorage = Depends(GetEventStorage),
) -> EventModel:
    return await event_storage.update(
        event_id=event_id,
        update_event=update_event,
    )


@router.delete("/{event_id}", status_code=204)
async def delete_event(
    event_id: int,
    response: Response,
    event_storage: IEventStorage = Depends(GetEventStorage),
) -> Response:
    await event_storage.delete(event_id=event_id)
    response.status_code = HTTPStatus.NO_CONTENT
    return response
