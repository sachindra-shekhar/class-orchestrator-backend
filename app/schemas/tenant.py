from datetime import datetime
from typing import Literal
from uuid import UUID

from pydantic import BaseModel, EmailStr

from app.schemas.common import ORMBase


class Tenant(ORMBase):
    id: UUID
    name: str
    email: EmailStr
    status: Literal["active", "inactive", "suspended"]
    createdAt: datetime
    updatedAt: datetime


class TenantCreate(BaseModel):
    name: str
    email: EmailStr


class TenantUpdate(BaseModel):
    name: str | None = None
    email: EmailStr | None = None
    status: Literal["active", "inactive", "suspended"] | None = None
