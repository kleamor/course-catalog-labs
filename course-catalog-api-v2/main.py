from typing import Literal

from fastapi import Depends, FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import func, select, update
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from db import get_db
from models import Course, Enrollment, Student
from schemas import CourseOut, CourseStats, EnrollmentDetail, EnrollmentIn, EnrollmentOut, StudentIn, StudentOut

app = FastAPI(title="Course Catalog API")
app.add_middleware(CORSMiddleware, allow_origins=["http://localhost:3000"], allow_methods=["*"], allow_headers=["*"])


def integrity_error(exc: IntegrityError) -> HTTPException:
    name = getattr(getattr(getattr(exc, "orig", None), "diag", None), "constraint_name", None)
    errors = {
        "students_email_key": (409, "A student with this email already exists"),
        "enrollments_course_id_student_id_key": (409, "Student is already enrolled in this course"),
        "enrollments_course_id_fkey": (404, "Course not found"),
        "enrollments_student_id_fkey": (404, "Student not found"),
    }
    status, detail = errors.get(name, (400, "Database constraint error"))
    return HTTPException(status_code=status, detail=detail)


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
        raise HTTPException(status_code=404, detail="Course not found")
    return course


@app.post("/courses/{course_id}/like", response_model=CourseOut)
def like_course(course_id: str, db: Session = Depends(get_db)):
    course = db.scalars(update(Course).where(Course.id == course_id).values(likes=Course.likes + 1).returning(Course)).one_or_none()
    if course is None:
        db.rollback()
        raise HTTPException(status_code=404, detail="Course not found")
    db.commit()
    db.refresh(course)
    return course


@app.post("/students", response_model=StudentOut, status_code=201)
def create_student(data: StudentIn, db: Session = Depends(get_db)):
    student = Student(**data.model_dump())
    db.add(student)
    try:
        db.commit()
    except IntegrityError as exc:
        db.rollback()
        raise integrity_error(exc) from exc
    db.refresh(student)
    return student


@app.post("/enrollments", response_model=EnrollmentOut, status_code=201)
def create_enrollment(data: EnrollmentIn, db: Session = Depends(get_db)):
    enrollment = Enrollment(**data.model_dump())
    db.add(enrollment)
    try:
        db.commit()
    except IntegrityError as exc:
        db.rollback()
        raise integrity_error(exc) from exc
    db.refresh(enrollment)
    return enrollment


@app.get("/enrollments", response_model=list[EnrollmentDetail])
def list_enrollments(db: Session = Depends(get_db)):
    stmt = select(Enrollment.id, Enrollment.course_id, Enrollment.student_id, Enrollment.enrolled_at, Course.title.label("course_title"), Student.name.label("student_name")).join(Enrollment.course).join(Enrollment.student).order_by(Enrollment.id)
    return [dict(row) for row in db.execute(stmt).mappings()]


@app.get("/stats/courses", response_model=list[CourseStats])
def course_stats(db: Session = Depends(get_db)):
    stmt = select(Course.id.label("course_id"), func.count(Enrollment.id).label("enrolled")).outerjoin(Course.enrollments).group_by(Course.id).order_by(Course.id)
    return [dict(row) for row in db.execute(stmt).mappings()]
