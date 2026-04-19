from fastapi import APIRouter

from app.api.v1.domain import router as class_router
from app.api.v1.tenants import router as tenant_router

router = APIRouter()
router.include_router(tenant_router)
router.include_router(class_router)
