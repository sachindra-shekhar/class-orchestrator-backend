from datetime import datetime
from uuid import UUID

from sqlalchemy import and_, or_, select

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
from app.repositories.base import BaseRepository


class DomainRepository(BaseRepository):
    def list_by_tenant(self, model: type, tenant_id: UUID) -> list:
        return self.list(model, model.tenant_id == tenant_id)

    def get_by_id_and_tenant(self, model: type, entity_id: UUID, tenant_id: UUID):
        return self.get_one(model, model.id == entity_id, model.tenant_id == tenant_id)

    def list_occurrences_for_instructor(self, tenant_id: UUID, instructor_id: UUID) -> list[Occurrence]:
        stmt = (
            select(Occurrence)
            .join(ClassInstructor, ClassInstructor.class_id == Occurrence.class_id)
            .where(Occurrence.tenant_id == tenant_id, ClassInstructor.instructor_id == instructor_id)
        )
        return list(self.db.scalars(stmt).all())

    def list_classes_for_instructor(self, tenant_id: UUID, instructor_id: UUID) -> list[ClassModel]:
        stmt = (
            select(ClassModel)
            .join(ClassInstructor, ClassInstructor.class_id == ClassModel.id)
            .where(ClassModel.tenant_id == tenant_id, ClassInstructor.instructor_id == instructor_id)
        )
        return list(self.db.scalars(stmt).all())

    def list_students_for_instructor(self, tenant_id: UUID, instructor_id: UUID) -> list[Student]:
        stmt = (
            select(Student)
            .join(Enrollment, Enrollment.student_id == Student.id)
            .join(ClassInstructor, ClassInstructor.class_id == Enrollment.class_id)
            .where(Student.tenant_id == tenant_id, ClassInstructor.instructor_id == instructor_id)
        )
        return list(self.db.scalars(stmt).all())

    def list_student_classes(self, tenant_id: UUID, student_id: UUID) -> list[ClassModel]:
        stmt = (
            select(ClassModel)
            .join(Enrollment, Enrollment.class_id == ClassModel.id)
            .where(ClassModel.tenant_id == tenant_id, Enrollment.student_id == student_id)
        )
        return list(self.db.scalars(stmt).all())

    def list_student_occurrences(self, tenant_id: UUID, student_id: UUID) -> list[Occurrence]:
        stmt = (
            select(Occurrence)
            .join(Enrollment, Enrollment.class_id == Occurrence.class_id)
            .where(Occurrence.tenant_id == tenant_id, Enrollment.student_id == student_id)
        )
        return list(self.db.scalars(stmt).all())

    def list_class_students(self, tenant_id: UUID, class_id: UUID) -> list[Student]:
        stmt = (
            select(Student)
            .join(ClassStudent, ClassStudent.student_id == Student.id)
            .where(Student.tenant_id == tenant_id, ClassStudent.class_id == class_id)
        )
        return list(self.db.scalars(stmt).all())

    def list_class_occurrences(self, tenant_id: UUID, class_id: UUID) -> list[Occurrence]:
        return self.list(Occurrence, Occurrence.tenant_id == tenant_id, Occurrence.class_id == class_id)

    def list_support_classes(self, tenant_id: UUID, support_id: UUID) -> list[ClassModel]:
        stmt = (
            select(ClassModel)
            .join(ClassSupport, ClassSupport.class_id == ClassModel.id)
            .where(ClassModel.tenant_id == tenant_id, ClassSupport.support_id == support_id)
        )
        return list(self.db.scalars(stmt).all())

    def list_attendance(self, tenant_id: UUID, occurrence_id: UUID) -> list[Attendance]:
        return self.list(Attendance, Attendance.tenant_id == tenant_id, Attendance.occurrence_id == occurrence_id)

    def find_occurrence_conflicts(self, tenant_id: UUID, start: datetime, end: datetime, exclude_id: UUID | None = None) -> list[Occurrence]:
        stmt = select(Occurrence).where(
            Occurrence.tenant_id == tenant_id,
            and_(Occurrence.start_time < end, Occurrence.end_time > start),
        )
        if exclude_id:
            stmt = stmt.where(Occurrence.id != exclude_id)
        return list(self.db.scalars(stmt).all())

    def find_timeslot_conflicts(self, tenant_id: UUID, resource_type: str, resource_id: str, start: datetime, end: datetime, exclude_id: UUID | None = None) -> list[TimeSlot]:
        stmt = select(TimeSlot).where(
            TimeSlot.tenant_id == tenant_id,
            TimeSlot.resource_type == resource_type,
            TimeSlot.resource_id == resource_id,
            and_(TimeSlot.start_time < end, TimeSlot.end_time > start),
        )
        if exclude_id:
            stmt = stmt.where(TimeSlot.id != exclude_id)
        return list(self.db.scalars(stmt).all())
