from fastapi import APIRouter

from tth.rest.api.v1.events import router as events_router
from tth.rest.api.v1.monitoring import router as monitoring_router
from tth.rest.api.v1.users import router as users_router

router = APIRouter(prefix="/v1")
router.include_router(monitoring_router)
router.include_router(users_router)
router.include_router(events_router)
