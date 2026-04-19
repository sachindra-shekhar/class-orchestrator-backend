from uuid import UUID

from app.models.entities import Tenant
from app.repositories.base import BaseRepository


class TenantRepository(BaseRepository):
    def list_tenants(self) -> list[Tenant]:
        return self.list(Tenant)

    def get_tenant(self, tenant_id: UUID) -> Tenant | None:
        return self.get_one(Tenant, Tenant.id == tenant_id)

    def get_tenant_by_email(self, email: str) -> Tenant | None:
        return self.get_one(Tenant, Tenant.email == email)
