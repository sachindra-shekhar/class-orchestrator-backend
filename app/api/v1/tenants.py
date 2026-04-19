from uuid import UUID

from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.orm import Session

from app.core.deps import get_db
from app.repositories.tenant_repo import TenantRepository
from app.schemas.tenant import Tenant, TenantCreate, TenantUpdate
from app.services.tenant_service import TenantService

router = APIRouter(prefix="/tenants", tags=["tenants"])


def tenant_service(db: Session = Depends(get_db)) -> TenantService:
    return TenantService(TenantRepository(db))


@router.post("", response_model=Tenant, status_code=status.HTTP_201_CREATED)
def create_tenant(payload: TenantCreate, service: TenantService = Depends(tenant_service)):
    tenant = service.create(payload)
    return {
        "id": tenant.id,
        "name": tenant.name,
        "email": tenant.email,
        "status": tenant.status,
        "createdAt": tenant.created_at,
        "updatedAt": tenant.updated_at,
    }


@router.get("", response_model=list[Tenant])
def list_tenants(service: TenantService = Depends(tenant_service)):
    tenants = service.list()
    return [
        {
            "id": tenant.id,
            "name": tenant.name,
            "email": tenant.email,
            "status": tenant.status,
            "createdAt": tenant.created_at,
            "updatedAt": tenant.updated_at,
        }
        for tenant in tenants
    ]


@router.get("/{tenantId}", response_model=Tenant)
def get_tenant(tenantId: UUID, service: TenantService = Depends(tenant_service)):
    tenant = service.get(tenantId)
    return {
        "id": tenant.id,
        "name": tenant.name,
        "email": tenant.email,
        "status": tenant.status,
        "createdAt": tenant.created_at,
        "updatedAt": tenant.updated_at,
    }


@router.put("/{tenantId}", response_model=Tenant)
def update_tenant(tenantId: UUID, payload: TenantUpdate, service: TenantService = Depends(tenant_service)):
    tenant = service.update(tenantId, payload)
    return {
        "id": tenant.id,
        "name": tenant.name,
        "email": tenant.email,
        "status": tenant.status,
        "createdAt": tenant.created_at,
        "updatedAt": tenant.updated_at,
    }


@router.delete("/{tenantId}", status_code=status.HTTP_204_NO_CONTENT)
def delete_tenant(tenantId: UUID, service: TenantService = Depends(tenant_service)) -> Response:
    service.delete(tenantId)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
