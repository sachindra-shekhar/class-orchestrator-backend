from uuid import UUID

from fastapi import APIRouter, Depends, Query, Response, status
from sqlalchemy.orm import Session

from app.core.deps import get_db
from app.models.entities import (
    ClassModel,
    CompensationRequest,
    Enrollment,
    Instructor,
    Location,
    Occurrence,
    Student,
    SupportStaff,
    TimeSlot,
)
from app.repositories.domain_repo import DomainRepository
from app.schemas.common import DataPage, Pagination
from app.schemas.domain import (
    AttendanceMark,
    AttendanceOut,
    BasicCreate,
    BasicUpdate,
    ClassCreate,
    ClassOut,
    ClassUpdate,
    CompensationRequestCreate,
    CompensationRequestOut,
    CompensationRequestPatch,
    EnrollmentCreate,
    EnrollmentOut,
    IdMutation,
    InstructorOut,
    LocationCreate,
    LocationOut,
    OccurrenceCreate,
    OccurrenceOut,
    OccurrenceUpdate,
    SkillMutation,
    StudentOut,
    TimeSlotCreate,
    TimeSlotOut,
)
from app.services.domain_service import DomainService

router = APIRouter(prefix="/tenants/{tenantId}", tags=["class-management"])


def domain_service(db: Session = Depends(get_db)) -> DomainService:
    return DomainService(DomainRepository(db))


def paged(data: list) -> dict:
    return {"data": data, "pagination": {"page": 1, "size": len(data), "total": len(data)}}


@router.get("/instructors", response_model=DataPage)
def list_instructors(tenantId: UUID, service: DomainService = Depends(domain_service)):
    return paged(service.list_basic(Instructor, tenantId))


@router.post("/instructors", response_model=InstructorOut, status_code=status.HTTP_201_CREATED)
def create_instructor(tenantId: UUID, payload: BasicCreate, service: DomainService = Depends(domain_service)):
    return service.create_basic(Instructor, tenantId, payload)


@router.get("/instructors/{instructorId}", response_model=InstructorOut)
def get_instructor(tenantId: UUID, instructorId: UUID, service: DomainService = Depends(domain_service)):
    return service.get_basic(Instructor, tenantId, instructorId)


@router.delete("/instructors/{instructorId}", status_code=status.HTTP_204_NO_CONTENT)
def delete_instructor(tenantId: UUID, instructorId: UUID, service: DomainService = Depends(domain_service)):
    service.delete_basic(Instructor, tenantId, instructorId)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.post("/instructors/{instructorId}/skills", status_code=status.HTTP_201_CREATED)
def add_skill(tenantId: UUID, instructorId: UUID, payload: SkillMutation, service: DomainService = Depends(domain_service)):
    skill = service.add_skill(tenantId, instructorId, payload.skill)
    return {"id": skill.id, "instructorId": instructorId, "skill": skill.skill}


@router.delete("/instructors/{instructorId}/skills", status_code=status.HTTP_204_NO_CONTENT)
def remove_skill(tenantId: UUID, instructorId: UUID, payload: SkillMutation, service: DomainService = Depends(domain_service)):
    service.remove_skill(tenantId, instructorId, payload.skill)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.get("/instructors/{instructorId}/classes", response_model=list[ClassOut])
def list_instructor_classes(tenantId: UUID, instructorId: UUID, service: DomainService = Depends(domain_service)):
    return service.repo.list_classes_for_instructor(tenantId, instructorId)


@router.get("/instructors/{instructorId}/occurrences", response_model=list[OccurrenceOut])
def list_instructor_occurrences(tenantId: UUID, instructorId: UUID, service: DomainService = Depends(domain_service)):
    return service.repo.list_occurrences_for_instructor(tenantId, instructorId)


@router.get("/instructors/{instructorId}/students", response_model=list[StudentOut])
def list_instructor_students(tenantId: UUID, instructorId: UUID, service: DomainService = Depends(domain_service)):
    return service.repo.list_students_for_instructor(tenantId, instructorId)


@router.get("/students", response_model=DataPage)
def list_students(tenantId: UUID, service: DomainService = Depends(domain_service)):
    return paged(service.list_basic(Student, tenantId))


@router.post("/students", response_model=StudentOut, status_code=status.HTTP_201_CREATED)
def create_student(tenantId: UUID, payload: BasicCreate, service: DomainService = Depends(domain_service)):
    return service.create_basic(Student, tenantId, payload)


@router.get("/students/{studentId}", response_model=StudentOut)
def get_student(tenantId: UUID, studentId: UUID, service: DomainService = Depends(domain_service)):
    return service.get_basic(Student, tenantId, studentId)


@router.put("/students/{studentId}", response_model=StudentOut)
def update_student(tenantId: UUID, studentId: UUID, payload: BasicUpdate, service: DomainService = Depends(domain_service)):
    return service.update_basic(Student, tenantId, studentId, payload)


@router.delete("/students/{studentId}", status_code=status.HTTP_204_NO_CONTENT)
def delete_student(tenantId: UUID, studentId: UUID, service: DomainService = Depends(domain_service)):
    service.delete_basic(Student, tenantId, studentId)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.get("/students/{studentId}/classes", response_model=list[ClassOut])
def student_classes(tenantId: UUID, studentId: UUID, service: DomainService = Depends(domain_service)):
    return service.repo.list_student_classes(tenantId, studentId)


@router.get("/students/{studentId}/occurrences", response_model=list[OccurrenceOut])
def student_occurrences(tenantId: UUID, studentId: UUID, service: DomainService = Depends(domain_service)):
    return service.repo.list_student_occurrences(tenantId, studentId)


@router.get("/students/{studentId}/enrollments", response_model=list[EnrollmentOut])
def student_enrollments(tenantId: UUID, studentId: UUID, service: DomainService = Depends(domain_service)):
    return service.repo.list(Enrollment, Enrollment.tenant_id == tenantId, Enrollment.student_id == studentId)


@router.post("/students/{studentId}/enrollments", response_model=EnrollmentOut, status_code=status.HTTP_201_CREATED)
def create_student_enrollment(tenantId: UUID, studentId: UUID, payload: EnrollmentCreate, service: DomainService = Depends(domain_service)):
    request = EnrollmentCreate(classId=payload.classId, studentId=studentId)
    return service.create_enrollment(tenantId, request)


@router.get("/classes", response_model=DataPage)
def list_classes(tenantId: UUID, service: DomainService = Depends(domain_service)):
    return paged(service.list_basic(ClassModel, tenantId))


@router.post("/classes", response_model=ClassOut, status_code=status.HTTP_201_CREATED)
def create_class(tenantId: UUID, payload: ClassCreate, service: DomainService = Depends(domain_service)):
    return service.create_class(tenantId, payload)


@router.get("/classes/{classId}", response_model=ClassOut)
def get_class(tenantId: UUID, classId: UUID, service: DomainService = Depends(domain_service)):
    return service.get_basic(ClassModel, tenantId, classId)


@router.put("/classes/{classId}", response_model=ClassOut)
def update_class(tenantId: UUID, classId: UUID, payload: ClassUpdate, service: DomainService = Depends(domain_service)):
    return service.update_class(tenantId, classId, payload)


@router.delete("/classes/{classId}", status_code=status.HTTP_204_NO_CONTENT)
def delete_class(tenantId: UUID, classId: UUID, service: DomainService = Depends(domain_service)):
    service.delete_basic(ClassModel, tenantId, classId)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.get("/classes/{classId}/occurrences", response_model=list[OccurrenceOut])
def class_occurrences(tenantId: UUID, classId: UUID, service: DomainService = Depends(domain_service)):
    return service.repo.list_class_occurrences(tenantId, classId)


@router.post("/classes/{classId}/occurrences", response_model=OccurrenceOut, status_code=status.HTTP_201_CREATED)
def create_occurrence(tenantId: UUID, classId: UUID, payload: OccurrenceCreate, service: DomainService = Depends(domain_service)):
    req = OccurrenceCreate(classId=classId, startTime=payload.startTime, endTime=payload.endTime, locationId=payload.locationId)
    return service.create_occurrence(tenantId, req)


@router.get("/occurrences/{occurrenceId}", response_model=OccurrenceOut)
def get_occurrence(tenantId: UUID, occurrenceId: UUID, service: DomainService = Depends(domain_service)):
    return service.get_basic(Occurrence, tenantId, occurrenceId)


@router.put("/occurrences/{occurrenceId}", response_model=OccurrenceOut)
def update_occurrence(tenantId: UUID, occurrenceId: UUID, payload: OccurrenceUpdate, service: DomainService = Depends(domain_service)):
    return service.update_occurrence(tenantId, occurrenceId, payload)


@router.get("/classes/{classId}/students", response_model=list[StudentOut])
def class_students(tenantId: UUID, classId: UUID, service: DomainService = Depends(domain_service)):
    return service.repo.list_class_students(tenantId, classId)


@router.post("/classes/{classId}/students", status_code=status.HTTP_201_CREATED)
def add_class_student(tenantId: UUID, classId: UUID, payload: IdMutation, service: DomainService = Depends(domain_service)):
    link = service.add_class_student(tenantId, classId, payload.id)
    return {"id": link.id, "classId": classId, "studentId": payload.id}


@router.delete("/classes/{classId}/students", status_code=status.HTTP_204_NO_CONTENT)
def remove_class_student(tenantId: UUID, classId: UUID, studentId: UUID = Query(...), service: DomainService = Depends(domain_service)):
    service.remove_class_student(tenantId, classId, studentId)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.post("/classes/{classId}/instructors", status_code=status.HTTP_201_CREATED)
def add_class_instructor(tenantId: UUID, classId: UUID, payload: IdMutation, service: DomainService = Depends(domain_service)):
    link = service.add_class_instructor(tenantId, classId, payload.id)
    return {"id": link.id, "classId": classId, "instructorId": payload.id}


@router.delete("/classes/{classId}/instructors", status_code=status.HTTP_204_NO_CONTENT)
def remove_class_instructor(tenantId: UUID, classId: UUID, instructorId: UUID = Query(...), service: DomainService = Depends(domain_service)):
    service.remove_class_instructor(tenantId, classId, instructorId)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.post("/classes/{classId}/support", status_code=status.HTTP_201_CREATED)
def add_class_support(tenantId: UUID, classId: UUID, payload: IdMutation, service: DomainService = Depends(domain_service)):
    link = service.add_class_support(tenantId, classId, payload.id)
    return {"id": link.id, "classId": classId, "supportId": payload.id}


@router.delete("/classes/{classId}/support", status_code=status.HTTP_204_NO_CONTENT)
def remove_class_support(tenantId: UUID, classId: UUID, supportId: UUID = Query(...), service: DomainService = Depends(domain_service)):
    service.remove_class_support(tenantId, classId, supportId)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.get("/support", response_model=DataPage)
def list_support(tenantId: UUID, service: DomainService = Depends(domain_service)):
    return paged(service.list_basic(SupportStaff, tenantId))


@router.get("/support/{supportId}/classes", response_model=list[ClassOut])
def classes_for_support(tenantId: UUID, supportId: UUID, service: DomainService = Depends(domain_service)):
    return service.repo.list_support_classes(tenantId, supportId)


@router.post("/enrollments/{enrollmentId}/compensations", response_model=CompensationRequestOut, status_code=status.HTTP_201_CREATED)
def create_compensation(tenantId: UUID, enrollmentId: UUID, payload: CompensationRequestCreate, service: DomainService = Depends(domain_service)):
    return service.create_compensation_for_enrollment(tenantId, enrollmentId, payload.reason)


@router.post("/locations", response_model=LocationOut, status_code=status.HTTP_201_CREATED)
def create_location(tenantId: UUID, payload: LocationCreate, service: DomainService = Depends(domain_service)):
    return service.create_location(tenantId, payload)


@router.get("/locations", response_model=list[LocationOut])
def list_locations(tenantId: UUID, service: DomainService = Depends(domain_service)):
    return service.list_basic(Location, tenantId)


@router.put("/locations/{locationId}", response_model=LocationOut)
def update_location(tenantId: UUID, locationId: UUID, payload: LocationCreate, service: DomainService = Depends(domain_service)):
    return service.update_location(tenantId, locationId, payload)


@router.delete("/locations/{locationId}", status_code=status.HTTP_204_NO_CONTENT)
def delete_location(tenantId: UUID, locationId: UUID, service: DomainService = Depends(domain_service)):
    service.delete_basic(Location, tenantId, locationId)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.post("/timeslots", response_model=TimeSlotOut, status_code=status.HTTP_201_CREATED)
def create_timeslot(tenantId: UUID, payload: TimeSlotCreate, service: DomainService = Depends(domain_service)):
    return service.create_timeslot(tenantId, payload)


@router.get("/timeslots", response_model=list[TimeSlotOut])
def list_timeslots(tenantId: UUID, service: DomainService = Depends(domain_service)):
    return service.list_basic(TimeSlot, tenantId)


@router.put("/timeslots/{timeslotId}", response_model=TimeSlotOut)
def update_timeslot(tenantId: UUID, timeslotId: UUID, payload: TimeSlotCreate, service: DomainService = Depends(domain_service)):
    return service.update_timeslot(tenantId, timeslotId, payload)


@router.delete("/timeslots/{timeslotId}", status_code=status.HTTP_204_NO_CONTENT)
def delete_timeslot(tenantId: UUID, timeslotId: UUID, service: DomainService = Depends(domain_service)):
    service.delete_basic(TimeSlot, tenantId, timeslotId)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/occurrences/{occurrenceId}/attendance", response_model=AttendanceOut)
def mark_attendance(tenantId: UUID, occurrenceId: UUID, payload: AttendanceMark, service: DomainService = Depends(domain_service)):
    return service.mark_attendance(tenantId, occurrenceId, payload)


@router.get("/occurrences/{occurrenceId}/attendance", response_model=list[AttendanceOut])
def get_attendance(tenantId: UUID, occurrenceId: UUID, service: DomainService = Depends(domain_service)):
    return service.repo.list_attendance(tenantId, occurrenceId)


@router.post("/compensation-requests", response_model=CompensationRequestOut, status_code=status.HTTP_201_CREATED)
def create_compensation_request(tenantId: UUID, payload: CompensationRequestCreate, service: DomainService = Depends(domain_service)):
    return service.create_compensation_request(tenantId, payload)


@router.get("/compensation-requests", response_model=list[CompensationRequestOut])
def list_compensation_requests(tenantId: UUID, service: DomainService = Depends(domain_service)):
    return service.list_basic(CompensationRequest, tenantId)


@router.patch("/compensation-requests/{requestId}", response_model=CompensationRequestOut)
def patch_compensation_request(tenantId: UUID, requestId: UUID, payload: CompensationRequestPatch, service: DomainService = Depends(domain_service)):
    return service.patch_compensation_request(tenantId, requestId, payload.status)


@router.get("/reports/attendance")
def attendance_report(tenantId: UUID, service: DomainService = Depends(domain_service)):
    attendance = service.repo.list(Attendance, Attendance.tenant_id == tenantId)
    return {"tenantId": tenantId, "totalRecords": len(attendance), "data": attendance}


@router.get("/reports/enrollment")
def enrollment_report(tenantId: UUID, service: DomainService = Depends(domain_service)):
    enrollments = service.repo.list(Enrollment, Enrollment.tenant_id == tenantId)
    return {"tenantId": tenantId, "totalRecords": len(enrollments), "data": enrollments}
