"""create catalog tables

Revision ID: 0001
Revises:
Create Date: 2026-11-20
"""

from alembic import op
import sqlalchemy as sa


revision = "0001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "courses",
        sa.Column("id", sa.Text(), nullable=False),
        sa.Column("title", sa.Text(), nullable=False),
        sa.Column("description", sa.Text(), nullable=False),
        sa.Column("credits", sa.Integer(), nullable=False),
        sa.Column("is_elective", sa.Boolean(), server_default=sa.text("false"), nullable=False),
        sa.Column("likes", sa.Integer(), server_default=sa.text("0"), nullable=False),
        sa.CheckConstraint("credits > 0", name="courses_credits_check"),
        sa.CheckConstraint("likes >= 0", name="courses_likes_check"),
        sa.PrimaryKeyConstraint("id", name="courses_pkey"),
    )
    op.create_table(
        "students",
        sa.Column("id", sa.BigInteger(), sa.Identity(always=True), nullable=False),
        sa.Column("name", sa.Text(), nullable=False),
        sa.Column("email", sa.Text(), nullable=False),
        sa.CheckConstraint("length(name) >= 2", name="students_name_check"),
        sa.CheckConstraint("position('@' IN email) > 1", name="students_email_format_check"),
        sa.PrimaryKeyConstraint("id", name="students_pkey"),
        sa.UniqueConstraint("email", name="students_email_key"),
    )
    op.create_table(
        "enrollments",
        sa.Column("id", sa.BigInteger(), sa.Identity(always=True), nullable=False),
        sa.Column("course_id", sa.Text(), nullable=False),
        sa.Column("student_id", sa.BigInteger(), nullable=False),
        sa.Column("enrolled_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.ForeignKeyConstraint(["course_id"], ["courses.id"], name="enrollments_course_id_fkey", ondelete="RESTRICT"),
        sa.ForeignKeyConstraint(["student_id"], ["students.id"], name="enrollments_student_id_fkey", ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id", name="enrollments_pkey"),
        sa.UniqueConstraint("course_id", "student_id", name="enrollments_course_id_student_id_key"),
    )
    op.create_index("enrollments_student_id_idx", "enrollments", ["student_id"])


def downgrade() -> None:
    op.drop_index("enrollments_student_id_idx", table_name="enrollments")
    op.drop_table("enrollments")
    op.drop_table("students")
    op.drop_table("courses")
