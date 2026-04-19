from datetime import datetime
from uuid import UUID

from app.core.errors import NotFoundError, ScheduleConflictError
from app.models.entities import (
    Attendance,
    ClassInstructor,
    ClassModel,
    ClassStudent,
    ClassSupport,
    CompensationRequest,
    Enrollment,
    Instructor,
    InstructorSkill,
    Location,
    Occurrence,
    Student,
    SupportStaff,
    TimeSlot,
)
from app.repositories.domain_repo import DomainRepository
from app.schemas.domain import (
    AttendanceMark,
    BasicCreate,
    BasicUpdate,
    ClassCreate,
    ClassUpdate,
    CompensationRequestCreate,
    EnrollmentCreate,
    LocationCreate,
    OccurrenceCreate,
    OccurrenceUpdate,
    TimeSlotCreate,
)


class DomainService:
    def __init__(self, repo: DomainRepository) -> None:
        self.repo = repo

    def create_basic(self, model: type, tenant_id: UUID, payload: BasicCreate):
        return self.repo.create(model(tenant_id=tenant_id, name=payload.name, email=payload.email or ""))

    def list_basic(self, model: type, tenant_id: UUID):
        return self.repo.list_by_tenant(model, tenant_id)

    def get_basic(self, model: type, tenant_id: UUID, entity_id: UUID):
        entity = self.repo.get_by_id_and_tenant(model, entity_id, tenant_id)
        if not entity:
            raise NotFoundError(f"{model.__name__} not found")
        return entity

    def update_basic(self, model: type, tenant_id: UUID, entity_id: UUID, payload: BasicUpdate):
        entity = self.get_basic(model, tenant_id, entity_id)
        if payload.name is not None:
            entity.name = payload.name
        if payload.email is not None and hasattr(entity, "email"):
            entity.email = payload.email
        if payload.status is not None and hasattr(entity, "status"):
            entity.status = payload.status
        self.repo.db.flush()
        self.repo.db.refresh(entity)
        return entity

    def delete_basic(self, model: type, tenant_id: UUID, entity_id: UUID):
        entity = self.get_basic(model, tenant_id, entity_id)
        self.repo.delete(entity)

    def add_skill(self, tenant_id: UUID, instructor_id: UUID, skill: str):
        self.get_basic(Instructor, tenant_id, instructor_id)
        return self.repo.create(InstructorSkill(instructor_id=instructor_id, skill=skill))

    def remove_skill(self, tenant_id: UUID, instructor_id: UUID, skill: str) -> None:
        self.get_basic(Instructor, tenant_id, instructor_id)
        skills = self.repo.list(InstructorSkill, InstructorSkill.instructor_id == instructor_id, InstructorSkill.skill == skill)
        for item in skills:
            self.repo.delete(item)

    def create_class(self, tenant_id: UUID, payload: ClassCreate):
        return self.repo.create(ClassModel(tenant_id=tenant_id, name=payload.name, description=payload.description))

    def update_class(self, tenant_id: UUID, class_id: UUID, payload: ClassUpdate):
        cls = self.get_basic(ClassModel, tenant_id, class_id)
        if payload.name is not None:
            cls.name = payload.name
        if payload.description is not None:
            cls.description = payload.description
        self.repo.db.flush()
        self.repo.db.refresh(cls)
        return cls

    def _ensure_no_conflict(self, tenant_id: UUID, start: datetime, end: datetime, exclude_id: UUID | None = None):
        conflicts = self.repo.find_occurrence_conflicts(tenant_id, start, end, exclude_id=exclude_id)
        if conflicts:
            raise ScheduleConflictError(
                "Schedule conflict detected",
                details={
                    "conflictingOccurrenceIds": [str(item.id) for item in conflicts],
                },
            )

    def create_occurrence(self, tenant_id: UUID, payload: OccurrenceCreate):
        self.get_basic(ClassModel, tenant_id, payload.classId)
        self._ensure_no_conflict(tenant_id, payload.startTime, payload.endTime)
        return self.repo.create(
            Occurrence(
                tenant_id=tenant_id,
                class_id=payload.classId,
                start_time=payload.startTime,
                end_time=payload.endTime,
                location_id=payload.locationId,
                status="scheduled",
            )
        )

    def update_occurrence(self, tenant_id: UUID, occurrence_id: UUID, payload: OccurrenceUpdate):
        occ = self.get_basic(Occurrence, tenant_id, occurrence_id)
        start = payload.startTime or occ.start_time
        end = payload.endTime or occ.end_time
        if payload.startTime is not None or payload.endTime is not None:
            self._ensure_no_conflict(tenant_id, start, end, exclude_id=occurrence_id)
        occ.start_time = start
        occ.end_time = end
        if payload.status is not None:
            occ.status = payload.status
        self.repo.db.flush()
        self.repo.db.refresh(occ)
        return occ

    def create_enrollment(self, tenant_id: UUID, payload: EnrollmentCreate):
        self.get_basic(ClassModel, tenant_id, payload.classId)
        self.get_basic(Student, tenant_id, payload.studentId)
        return self.repo.create(Enrollment(tenant_id=tenant_id, class_id=payload.classId, student_id=payload.studentId, status="active"))

    def add_class_student(self, tenant_id: UUID, class_id: UUID, student_id: UUID):
        self.get_basic(ClassModel, tenant_id, class_id)
        self.get_basic(Student, tenant_id, student_id)
        return self.repo.create(ClassStudent(class_id=class_id, student_id=student_id))

    def remove_class_student(self, tenant_id: UUID, class_id: UUID, student_id: UUID):
        links = self.repo.list(ClassStudent, ClassStudent.class_id == class_id, ClassStudent.student_id == student_id)
        for item in links:
            self.repo.delete(item)

    def add_class_instructor(self, tenant_id: UUID, class_id: UUID, instructor_id: UUID):
        self.get_basic(ClassModel, tenant_id, class_id)
        self.get_basic(Instructor, tenant_id, instructor_id)
        return self.repo.create(ClassInstructor(class_id=class_id, instructor_id=instructor_id))

    def remove_class_instructor(self, tenant_id: UUID, class_id: UUID, instructor_id: UUID):
        links = self.repo.list(ClassInstructor, ClassInstructor.class_id == class_id, ClassInstructor.instructor_id == instructor_id)
        for item in links:
            self.repo.delete(item)

    def add_class_support(self, tenant_id: UUID, class_id: UUID, support_id: UUID):
        self.get_basic(ClassModel, tenant_id, class_id)
        self.get_basic(SupportStaff, tenant_id, support_id)
        return self.repo.create(ClassSupport(class_id=class_id, support_id=support_id))

    def remove_class_support(self, tenant_id: UUID, class_id: UUID, support_id: UUID):
        links = self.repo.list(ClassSupport, ClassSupport.class_id == class_id, ClassSupport.support_id == support_id)
        for item in links:
            self.repo.delete(item)

    def create_location(self, tenant_id: UUID, payload: LocationCreate):
        return self.repo.create(Location(tenant_id=tenant_id, name=payload.name, address=payload.address))

    def update_location(self, tenant_id: UUID, location_id: UUID, payload: LocationCreate):
        loc = self.get_basic(Location, tenant_id, location_id)
        loc.name = payload.name
        loc.address = payload.address
        self.repo.db.flush()
        self.repo.db.refresh(loc)
        return loc

    def create_timeslot(self, tenant_id: UUID, payload: TimeSlotCreate):
        conflicts = self.repo.find_timeslot_conflicts(tenant_id, payload.resourceType, payload.resourceId, payload.startTime, payload.endTime)
        if conflicts:
            raise ScheduleConflictError("Schedule conflict detected", details={"conflictingTimeSlotIds": [str(i.id) for i in conflicts]})
        return self.repo.create(
            TimeSlot(
                tenant_id=tenant_id,
                resource_type=payload.resourceType,
                resource_id=payload.resourceId,
                start_time=payload.startTime,
                end_time=payload.endTime,
            )
        )

    def update_timeslot(self, tenant_id: UUID, timeslot_id: UUID, payload: TimeSlotCreate):
        slot = self.get_basic(TimeSlot, tenant_id, timeslot_id)
        conflicts = self.repo.find_timeslot_conflicts(
            tenant_id,
            payload.resourceType,
            payload.resourceId,
            payload.startTime,
            payload.endTime,
            exclude_id=timeslot_id,
        )
        if conflicts:
            raise ScheduleConflictError("Schedule conflict detected", details={"conflictingTimeSlotIds": [str(i.id) for i in conflicts]})
        slot.resource_type = payload.resourceType
        slot.resource_id = payload.resourceId
        slot.start_time = payload.startTime
        slot.end_time = payload.endTime
        self.repo.db.flush()
        self.repo.db.refresh(slot)
        return slot

    def mark_attendance(self, tenant_id: UUID, occurrence_id: UUID, payload: AttendanceMark):
        self.get_basic(Occurrence, tenant_id, occurrence_id)
        self.get_basic(Student, tenant_id, payload.studentId)
        existing = self.repo.get_one(
            Attendance,
            Attendance.tenant_id == tenant_id,
            Attendance.occurrence_id == occurrence_id,
            Attendance.student_id == payload.studentId,
        )
        if existing:
            existing.status = payload.status
            self.repo.db.flush()
            self.repo.db.refresh(existing)
            return existing
        return self.repo.create(
            Attendance(
                tenant_id=tenant_id,
                occurrence_id=occurrence_id,
                student_id=payload.studentId,
                status=payload.status,
            )
        )

    def create_compensation_request(self, tenant_id: UUID, payload: CompensationRequestCreate):
        self.get_basic(Enrollment, tenant_id, payload.enrollmentId)
        return self.repo.create(
            CompensationRequest(
                tenant_id=tenant_id,
                enrollment_id=payload.enrollmentId,
                reason=payload.reason,
                status="pending",
            )
        )

    def patch_compensation_request(self, tenant_id: UUID, request_id: UUID, status: str):
        request = self.get_basic(CompensationRequest, tenant_id, request_id)
        request.status = status
        self.repo.db.flush()
        self.repo.db.refresh(request)
        return request

    def create_compensation_for_enrollment(self, tenant_id: UUID, enrollment_id: UUID, reason: str):
        self.get_basic(Enrollment, tenant_id, enrollment_id)
        return self.repo.create(CompensationRequest(tenant_id=tenant_id, enrollment_id=enrollment_id, reason=reason, status="pending"))
