from typing import Literal

from fastapi import Depends, FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from db import get_db
from counter import sql_query_header
from graphql_api import graphql_app
import problem
import services
from models import Course, Enrollment, Student
from schemas import CourseOut, CourseStats, EnrollmentDetail, EnrollmentIn, EnrollmentOut, StudentIn, StudentOut

app = FastAPI(title="Course Catalog API")
app.middleware("http")(sql_query_header)
problem.install(app)
app.include_router(graphql_app, prefix="/graphql")
app.add_middleware(CORSMiddleware, allow_origins=["http://localhost:3000"], allow_methods=["*"], allow_headers=["*"])


@app.get("/")
def read_root():
    return {"message": "Course Catalog API is running"}


@app.get("/courses", response_model=list[CourseOut])
def list_courses(page: int = Query(1, ge=1), size: int = Query(10, ge=1, le=100), is_elective: bool | None = None, sort: Literal["title", "popular"] = "popular", db: Session = Depends(get_db)):
    stmt = select(Course)
    if is_elective is not None:
        stmt = stmt.where(Course.is_elective == is_elective)
    order_by = (Course.title, Course.id) if sort == "title" else (Course.likes.desc(), Course.id)
    return list(db.scalars(stmt.order_by(*order_by).limit(size).offset((page - 1) * size)))


@app.get("/courses/{course_id}", response_model=CourseOut)
def get_course(course_id: str, db: Session = Depends(get_db)):
    course = db.get(Course, course_id)
    if course is None:
        raise services.ServiceError("COURSE_NOT_FOUND", "Course not found")
    return course


@app.post("/courses/{course_id}/like", response_model=CourseOut)
def like_course(course_id: str, db: Session = Depends(get_db)):
    return services.like_course(db, course_id)


@app.post("/students", response_model=StudentOut, status_code=201)
def create_student(data: StudentIn, db: Session = Depends(get_db)):
    return services.create_student(db, data.name, data.email)


@app.post("/enrollments", response_model=EnrollmentOut, status_code=201)
def create_enrollment(data: EnrollmentIn, db: Session = Depends(get_db)):
    return services.enroll(db, data.course_id, data.student_id)


@app.get("/enrollments", response_model=list[EnrollmentDetail])
def list_enrollments(db: Session = Depends(get_db)):
    stmt = select(Enrollment.id, Enrollment.course_id, Enrollment.student_id, Enrollment.enrolled_at, Course.title.label("course_title"), Student.name.label("student_name")).join(Enrollment.course).join(Enrollment.student).order_by(Enrollment.id)
    return [dict(row) for row in db.execute(stmt).mappings()]


@app.get("/students", response_model=list[StudentOut])
def list_students(db: Session = Depends(get_db)):
    return list(db.scalars(select(Student).order_by(Student.id)))


@app.get("/stats/courses", response_model=list[CourseStats])
def course_stats(db: Session = Depends(get_db)):
    stmt = select(Course.id.label("course_id"), func.count(Enrollment.id).label("enrolled")).outerjoin(Course.enrollments).group_by(Course.id).order_by(Course.id)
    return [dict(row) for row in db.execute(stmt).mappings()]
