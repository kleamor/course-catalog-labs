"""GraphQL entrance to the same catalog database and services as REST."""
from datetime import datetime
from typing import Annotated

import strawberry
from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.orm import Session
from strawberry.dataloader import DataLoader
from strawberry.extensions import DisableIntrospection, MaskErrors, MaxAliasesLimiter, QueryDepthLimiter
from strawberry.fastapi import BaseContext, GraphQLRouter
from strawberry.types import Info

import services
from db import get_db
from config import settings
from models import Course, Enrollment, Student


def ordered(keys, rows, key):
    lookup = {key(row): row for row in rows}
    return [lookup.get(item) for item in keys]


class Context(BaseContext):
    def __init__(self, db: Session):
        super().__init__()
        self.db = db
        self.courses = DataLoader(load_fn=self.load_courses)
        self.students = DataLoader(load_fn=self.load_students)
        self.enrollments = DataLoader(load_fn=self.load_enrollments)
        self.course_enrollments = DataLoader(load_fn=self.load_course_enrollments)

    async def load_courses(self, keys: list[str]) -> list[Course | None]:
        rows = self.db.scalars(select(Course).where(Course.id.in_(keys))).all()
        return ordered(keys, rows, lambda row: row.id)

    async def load_students(self, keys: list[int]) -> list[Student | None]:
        rows = self.db.scalars(select(Student).where(Student.id.in_(keys))).all()
        return ordered(keys, rows, lambda row: row.id)

    async def load_enrollments(self, keys: list[int]) -> list[list[Enrollment]]:
        rows = self.db.scalars(select(Enrollment).where(Enrollment.student_id.in_(keys)).order_by(Enrollment.id)).all()
        groups = {key: [] for key in keys}
        for row in rows:
            groups[row.student_id].append(row)
        return [groups[key] for key in keys]

    async def load_course_enrollments(self, keys: list[str]) -> list[list[Enrollment]]:
        rows = self.db.scalars(select(Enrollment).where(Enrollment.course_id.in_(keys)).order_by(Enrollment.id)).all()
        groups = {key: [] for key in keys}
        for row in rows:
            groups[row.course_id].append(row)
        return [groups[key] for key in keys]


def get_context(db: Annotated[Session, Depends(get_db)]) -> Context:
    return Context(db)


@strawberry.type(name="Course")
class CourseType:
    id: strawberry.ID
    title: str
    description: str
    credits: int
    is_elective: bool
    likes: int
    level: str

    @strawberry.field
    async def enrollments(self, info: Info) -> list["EnrollmentType"]:
        return await info.context.course_enrollments.load(self.id)


@strawberry.type(name="Student")
class StudentType:
    id: strawberry.ID
    name: str
    email: str

    @strawberry.field
    async def enrollments(self, info: Info) -> list["EnrollmentType"]:
        return await info.context.enrollments.load(int(self.id))


@strawberry.type(name="Enrollment")
class EnrollmentType:
    id: strawberry.ID
    enrolled_at: datetime

    @strawberry.field
    async def course(self, info: Info) -> CourseType:
        return await info.context.courses.load(self.course_id)

    @strawberry.field
    async def student(self, info: Info) -> StudentType:
        return await info.context.students.load(self.student_id)


@strawberry.type
class Query:
    @strawberry.field
    def courses(self, info: Info, is_elective: bool | None = None, limit: int = 20) -> list[CourseType]:
        if not 1 <= limit <= 100:
            raise ValueError("limit must be between 1 and 100")
        stmt = select(Course)
        if is_elective is not None:
            stmt = stmt.where(Course.is_elective == is_elective)
        return info.context.db.scalars(stmt.order_by(Course.likes.desc(), Course.id).limit(limit)).all()

    @strawberry.field
    def course(self, info: Info, id: strawberry.ID) -> CourseType | None:
        return info.context.db.get(Course, id)

    @strawberry.field
    def students(self, info: Info, limit: int = 20) -> list[StudentType]:
        if not 1 <= limit <= 100:
            raise ValueError("limit must be between 1 and 100")
        return info.context.db.scalars(select(Student).order_by(Student.id).limit(limit)).all()

    @strawberry.field
    def student(self, info: Info, id: strawberry.ID) -> StudentType | None:
        try:
            student_id = int(id)
        except ValueError:
            return None
        return info.context.db.get(Student, student_id)

    @strawberry.field
    def enrollments(self, info: Info, limit: int = 20) -> list[EnrollmentType]:
        if not 1 <= limit <= 100:
            raise ValueError("limit must be between 1 and 100")
        return info.context.db.scalars(select(Enrollment).order_by(Enrollment.id).limit(limit)).all()


@strawberry.type
class UserError:
    code: str
    message: str


@strawberry.input
class EnrollInput:
    course_id: strawberry.ID
    student_id: strawberry.ID


@strawberry.type
class EnrollPayload:
    enrollment: EnrollmentType | None = None
    user_errors: list[UserError] = strawberry.field(default_factory=list)


@strawberry.type
class LikePayload:
    course: CourseType | None = None
    user_errors: list[UserError] = strawberry.field(default_factory=list)


def as_user_errors(error: services.ServiceError) -> list[UserError]:
    return [UserError(code=error.code, message=error.message)]


@strawberry.type
class Mutation:
    @strawberry.mutation
    def enroll(self, info: Info, input: EnrollInput) -> EnrollPayload:
        try:
            return EnrollPayload(enrollment=services.enroll(info.context.db, input.course_id, int(input.student_id)))
        except services.ServiceError as error:
            return EnrollPayload(user_errors=as_user_errors(error))

    @strawberry.mutation
    def like_course(self, info: Info, id: strawberry.ID) -> LikePayload:
        try:
            return LikePayload(course=services.like_course(info.context.db, id))
        except services.ServiceError as error:
            return LikePayload(user_errors=as_user_errors(error))


extensions = [QueryDepthLimiter(max_depth=5), MaxAliasesLimiter(max_alias_count=10), MaskErrors(should_mask_error=lambda error: error.original_error is not None)]
if not settings.graphql_introspection:
    extensions.append(DisableIntrospection())
schema = strawberry.Schema(query=Query, mutation=Mutation, extensions=extensions)
graphql_app = GraphQLRouter(schema, context_getter=get_context)
