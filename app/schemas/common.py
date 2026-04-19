from datetime import datetime
from typing import Any
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class ORMBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class MessageResponse(BaseModel):
    message: str


class Pagination(BaseModel):
    page: int = 1
    size: int
    total: int


class DataPage(BaseModel):
    data: list[Any]
    pagination: Pagination


class EntityRef(BaseModel):
    id: UUID


class TimeRange(BaseModel):
    startTime: datetime
    endTime: datetime
