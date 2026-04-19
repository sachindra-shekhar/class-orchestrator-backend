"""initial schema

Revision ID: 0001_initial_schema
Revises:
Create Date: 2026-04-19 00:00:00

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "0001_initial_schema"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "tenants",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("email", sa.String(length=255), nullable=False),
        sa.Column("status", sa.Enum("active", "inactive", "suspended", name="tenant_status"), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("email"),
    )

    op.create_table(
        "instructors",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("tenant_id", sa.Uuid(), nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("email", sa.String(length=255), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["tenant_id"], ["tenants.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_instructors_tenant_id"), "instructors", ["tenant_id"], unique=False)

    op.create_table(
        "students",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("tenant_id", sa.Uuid(), nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("email", sa.String(length=255), nullable=False),
        sa.Column("status", sa.String(length=64), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["tenant_id"], ["tenants.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_students_tenant_id"), "students", ["tenant_id"], unique=False)

    op.create_table(
        "support_staff",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("tenant_id", sa.Uuid(), nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("email", sa.String(length=255), nullable=False),
        sa.ForeignKeyConstraint(["tenant_id"], ["tenants.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_support_staff_tenant_id"), "support_staff", ["tenant_id"], unique=False)

    op.create_table(
        "classes",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("tenant_id", sa.Uuid(), nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["tenant_id"], ["tenants.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_classes_tenant_id"), "classes", ["tenant_id"], unique=False)

    op.create_table(
        "locations",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("tenant_id", sa.Uuid(), nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("address", sa.String(length=500), nullable=True),
        sa.ForeignKeyConstraint(["tenant_id"], ["tenants.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_locations_tenant_id"), "locations", ["tenant_id"], unique=False)

    op.create_table(
        "occurrences",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("tenant_id", sa.Uuid(), nullable=False),
        sa.Column("class_id", sa.Uuid(), nullable=False),
        sa.Column("location_id", sa.Uuid(), nullable=True),
        sa.Column("start_time", sa.DateTime(timezone=True), nullable=False),
        sa.Column("end_time", sa.DateTime(timezone=True), nullable=False),
        sa.Column("status", sa.String(length=64), nullable=False),
        sa.ForeignKeyConstraint(["class_id"], ["classes.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["location_id"], ["locations.id"], ondelete="SET NULL"),
        sa.ForeignKeyConstraint(["tenant_id"], ["tenants.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_occurrences_class_id"), "occurrences", ["class_id"], unique=False)
    op.create_index(op.f("ix_occurrences_tenant_id"), "occurrences", ["tenant_id"], unique=False)

    op.create_table(
        "time_slots",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("tenant_id", sa.Uuid(), nullable=False),
        sa.Column("resource_type", sa.String(length=64), nullable=False),
        sa.Column("resource_id", sa.String(length=64), nullable=False),
        sa.Column("start_time", sa.DateTime(timezone=True), nullable=False),
        sa.Column("end_time", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["tenant_id"], ["tenants.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_time_slots_tenant_id"), "time_slots", ["tenant_id"], unique=False)

    op.create_table(
        "enrollments",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("tenant_id", sa.Uuid(), nullable=False),
        sa.Column("class_id", sa.Uuid(), nullable=False),
        sa.Column("student_id", sa.Uuid(), nullable=False),
        sa.Column("status", sa.String(length=64), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["class_id"], ["classes.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["student_id"], ["students.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["tenant_id"], ["tenants.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("class_id", "student_id", name="uq_class_student_enrollment"),
    )
    op.create_index(op.f("ix_enrollments_class_id"), "enrollments", ["class_id"], unique=False)
    op.create_index(op.f("ix_enrollments_student_id"), "enrollments", ["student_id"], unique=False)
    op.create_index(op.f("ix_enrollments_tenant_id"), "enrollments", ["tenant_id"], unique=False)

    op.create_table(
        "attendance",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("tenant_id", sa.Uuid(), nullable=False),
        sa.Column("occurrence_id", sa.Uuid(), nullable=False),
        sa.Column("student_id", sa.Uuid(), nullable=False),
        sa.Column("status", sa.String(length=64), nullable=False),
        sa.Column("marked_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["occurrence_id"], ["occurrences.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["student_id"], ["students.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["tenant_id"], ["tenants.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_attendance_occurrence_id"), "attendance", ["occurrence_id"], unique=False)
    op.create_index(op.f("ix_attendance_student_id"), "attendance", ["student_id"], unique=False)
    op.create_index(op.f("ix_attendance_tenant_id"), "attendance", ["tenant_id"], unique=False)

    op.create_table(
        "compensation_requests",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("tenant_id", sa.Uuid(), nullable=False),
        sa.Column("enrollment_id", sa.Uuid(), nullable=False),
        sa.Column("reason", sa.Text(), nullable=False),
        sa.Column("status", sa.String(length=64), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["enrollment_id"], ["enrollments.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["tenant_id"], ["tenants.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_compensation_requests_enrollment_id"), "compensation_requests", ["enrollment_id"], unique=False)
    op.create_index(op.f("ix_compensation_requests_tenant_id"), "compensation_requests", ["tenant_id"], unique=False)

    op.create_table(
        "instructor_skills",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("instructor_id", sa.Uuid(), nullable=False),
        sa.Column("skill", sa.String(length=255), nullable=False),
        sa.ForeignKeyConstraint(["instructor_id"], ["instructors.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("instructor_id", "skill", name="uq_instructor_skill"),
    )
    op.create_index(op.f("ix_instructor_skills_instructor_id"), "instructor_skills", ["instructor_id"], unique=False)

    op.create_table(
        "class_instructors",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("class_id", sa.Uuid(), nullable=False),
        sa.Column("instructor_id", sa.Uuid(), nullable=False),
        sa.ForeignKeyConstraint(["class_id"], ["classes.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["instructor_id"], ["instructors.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("class_id", "instructor_id", name="uq_class_instructor"),
    )
    op.create_index(op.f("ix_class_instructors_class_id"), "class_instructors", ["class_id"], unique=False)
    op.create_index(op.f("ix_class_instructors_instructor_id"), "class_instructors", ["instructor_id"], unique=False)

    op.create_table(
        "class_students",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("class_id", sa.Uuid(), nullable=False),
        sa.Column("student_id", sa.Uuid(), nullable=False),
        sa.ForeignKeyConstraint(["class_id"], ["classes.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["student_id"], ["students.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("class_id", "student_id", name="uq_class_student"),
    )
    op.create_index(op.f("ix_class_students_class_id"), "class_students", ["class_id"], unique=False)
    op.create_index(op.f("ix_class_students_student_id"), "class_students", ["student_id"], unique=False)

    op.create_table(
        "class_support",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("class_id", sa.Uuid(), nullable=False),
        sa.Column("support_id", sa.Uuid(), nullable=False),
        sa.ForeignKeyConstraint(["class_id"], ["classes.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["support_id"], ["support_staff.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("class_id", "support_id", name="uq_class_support"),
    )
    op.create_index(op.f("ix_class_support_class_id"), "class_support", ["class_id"], unique=False)
    op.create_index(op.f("ix_class_support_support_id"), "class_support", ["support_id"], unique=False)


def downgrade() -> None:
    op.drop_index(op.f("ix_class_support_support_id"), table_name="class_support")
    op.drop_index(op.f("ix_class_support_class_id"), table_name="class_support")
    op.drop_table("class_support")

    op.drop_index(op.f("ix_class_students_student_id"), table_name="class_students")
    op.drop_index(op.f("ix_class_students_class_id"), table_name="class_students")
    op.drop_table("class_students")

    op.drop_index(op.f("ix_class_instructors_instructor_id"), table_name="class_instructors")
    op.drop_index(op.f("ix_class_instructors_class_id"), table_name="class_instructors")
    op.drop_table("class_instructors")

    op.drop_index(op.f("ix_instructor_skills_instructor_id"), table_name="instructor_skills")
    op.drop_table("instructor_skills")

    op.drop_index(op.f("ix_compensation_requests_tenant_id"), table_name="compensation_requests")
    op.drop_index(op.f("ix_compensation_requests_enrollment_id"), table_name="compensation_requests")
    op.drop_table("compensation_requests")

    op.drop_index(op.f("ix_attendance_tenant_id"), table_name="attendance")
    op.drop_index(op.f("ix_attendance_student_id"), table_name="attendance")
    op.drop_index(op.f("ix_attendance_occurrence_id"), table_name="attendance")
    op.drop_table("attendance")

    op.drop_index(op.f("ix_enrollments_tenant_id"), table_name="enrollments")
    op.drop_index(op.f("ix_enrollments_student_id"), table_name="enrollments")
    op.drop_index(op.f("ix_enrollments_class_id"), table_name="enrollments")
    op.drop_table("enrollments")

    op.drop_index(op.f("ix_time_slots_tenant_id"), table_name="time_slots")
    op.drop_table("time_slots")

    op.drop_index(op.f("ix_occurrences_tenant_id"), table_name="occurrences")
    op.drop_index(op.f("ix_occurrences_class_id"), table_name="occurrences")
    op.drop_table("occurrences")

    op.drop_index(op.f("ix_locations_tenant_id"), table_name="locations")
    op.drop_table("locations")

    op.drop_index(op.f("ix_classes_tenant_id"), table_name="classes")
    op.drop_table("classes")

    op.drop_index(op.f("ix_support_staff_tenant_id"), table_name="support_staff")
    op.drop_table("support_staff")

    op.drop_index(op.f("ix_students_tenant_id"), table_name="students")
    op.drop_table("students")

    op.drop_index(op.f("ix_instructors_tenant_id"), table_name="instructors")
    op.drop_table("instructors")

    op.drop_table("tenants")
    sa.Enum(name="tenant_status").drop(op.get_bind(), checkfirst=False)
