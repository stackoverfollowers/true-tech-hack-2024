from collections.abc import Mapping

from fastapi import APIRouter, Depends, Security

from tth.common.estimations.estimator import Estimator
from tth.rest.auth.models import AuthUser
from tth.rest.overrides import REQUIRE_AUTH, GetEstimator

router = APIRouter(prefix="/estimations")


@router.get("/events/{event_id}")
async def event_estimation(
    event_id: int,
    auth_user: AuthUser = Security(REQUIRE_AUTH),
    estimator: Estimator = Depends(GetEstimator),
) -> Mapping[str, int]:
    return await estimator.estimate(
        user_id=auth_user.id,
        event_id=event_id,
    )
