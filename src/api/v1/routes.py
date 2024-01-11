from fastapi import APIRouter

from src.api.v1.endpoints.auth import router as auth_router
from src.api.v1.endpoints.billing import router as billing_router
from src.api.v1.endpoints.predictor import router as predictor_router

routers = APIRouter()
router_list = [
    auth_router,
    billing_router,
    predictor_router,
]

for router in router_list:
    router.tags = routers.tags.append("v1")
    routers.include_router(router)
