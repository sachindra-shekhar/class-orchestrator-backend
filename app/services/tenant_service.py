from uuid import UUID

from app.core.errors import BadRequestError, NotFoundError
from app.models.entities import Tenant
from app.repositories.tenant_repo import TenantRepository
from app.schemas.tenant import TenantCreate, TenantUpdate


class TenantService:
    def __init__(self, repo: TenantRepository) -> None:
        self.repo = repo

    def create(self, payload: TenantCreate) -> Tenant:
        if self.repo.get_tenant_by_email(payload.email):
            raise BadRequestError("Tenant with this email already exists")
        return self.repo.create(Tenant(name=payload.name, email=payload.email, status="active"))

    def list(self) -> list[Tenant]:
        return self.repo.list_tenants()

    def get(self, tenant_id: UUID) -> Tenant:
        tenant = self.repo.get_tenant(tenant_id)
        if not tenant:
            raise NotFoundError("Tenant not found")
        return tenant

    def update(self, tenant_id: UUID, payload: TenantUpdate) -> Tenant:
        tenant = self.get(tenant_id)
        if payload.name is not None:
            tenant.name = payload.name
        if payload.email is not None:
            tenant.email = payload.email
        if payload.status is not None:
            tenant.status = payload.status
        self.repo.db.flush()
        self.repo.db.refresh(tenant)
        return tenant

    def delete(self, tenant_id: UUID) -> None:
        tenant = self.repo.get_tenant(tenant_id)
        if not tenant:
            raise NotFoundError("Tenant not found")
        self.repo.delete(tenant)
