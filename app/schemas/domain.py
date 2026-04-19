from datetime import datetime
from typing import Literal
from uuid import UUID

from pydantic import BaseModel, EmailStr

from app.schemas.common import ORMBase


class BasicCreate(BaseModel):
    name: str
    email: EmailStr | None = None


class BasicUpdate(BaseModel):
    name: str | None = None
    email: EmailStr | None = None
    status: str | None = None


class InstructorOut(ORMBase):
    id: UUID
    tenant_id: UUID
    name: str
    email: str


class StudentOut(ORMBase):
    id: UUID
    tenant_id: UUID
    name: str
    email: str
    status: str


class ClassOut(ORMBase):
    id: UUID
    tenant_id: UUID
    name: str
    description: str | None = None


class OccurrenceCreate(BaseModel):
    classId: UUID
    startTime: datetime
    endTime: datetime
    locationId: UUID | None = None


class OccurrenceUpdate(BaseModel):
    startTime: datetime | None = None
    endTime: datetime | None = None
    status: str | None = None


class OccurrenceOut(ORMBase):
    id: UUID
    tenant_id: UUID
    class_id: UUID
    location_id: UUID | None = None
    start_time: datetime
    end_time: datetime
    status: str


class EnrollmentCreate(BaseModel):
    classId: UUID
    studentId: UUID


class EnrollmentOut(ORMBase):
    id: UUID
    tenant_id: UUID
    class_id: UUID
    student_id: UUID
    status: str


class AttendanceMark(BaseModel):
    studentId: UUID
    status: Literal["present", "absent", "late", "excused"]


class AttendanceOut(ORMBase):
    id: UUID
    tenant_id: UUID
    occurrence_id: UUID
    student_id: UUID
    status: str


class CompensationRequestCreate(BaseModel):
    enrollmentId: UUID
    reason: str


class CompensationRequestPatch(BaseModel):
    status: Literal["approved", "rejected"]


class CompensationRequestOut(ORMBase):
    id: UUID
    tenant_id: UUID
    enrollment_id: UUID
    reason: str
    status: str


class LocationOut(ORMBase):
    id: UUID
    tenant_id: UUID
    name: str
    address: str | None = None


class LocationCreate(BaseModel):
    name: str
    address: str | None = None


class TimeSlotCreate(BaseModel):
    resourceType: str
    resourceId: str
    startTime: datetime
    endTime: datetime


class TimeSlotOut(ORMBase):
    id: UUID
    tenant_id: UUID
    resource_type: str
    resource_id: str
    start_time: datetime
    end_time: datetime


class SkillMutation(BaseModel):
    skill: str


class IdMutation(BaseModel):
    id: UUID


class ClassCreate(BaseModel):
    name: str
    description: str | None = None


class ClassUpdate(BaseModel):
    name: str | None = None
    description: str | None = None
