from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from catalog import all_courses, course_by_id
from course_queries import (
    Page,
    SortOrder,
    filter_courses,
    paginate_courses,
    pagination,
    sort_courses,
)
from models import Course, Enrollment, EnrollmentIn


app = FastAPI(title="Course Catalog API")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)

ENROLLMENTS: list[Enrollment] = []


@app.get("/")
def read_root():
    return {"message": "Course Catalog API is running"}


@app.get("/courses", response_model=list[Course])
def list_courses(
    page: Annotated[Page, Depends(pagination)],
    is_elective: bool | None = None,
    sort: SortOrder = "popular",
) -> list[Course]:
    filtered_courses = filter_courses(all_courses(), is_elective)
    ordered_courses = sort_courses(filtered_courses, sort)
    return paginate_courses(ordered_courses, page)


@app.get("/courses/{course_id}", response_model=Course)
def get_course(course_id: str):
    course = course_by_id(course_id)
    if course is None:
        raise HTTPException(status_code=404, detail="Course not found")
    return course


@app.post("/courses/{course_id}/like", response_model=Course)
def like_course(course_id: str) -> Course:
    course = course_by_id(course_id)
    if course is None:
        raise HTTPException(status_code=404, detail="Course not found")
    course.likes += 1
    return course


@app.post("/enrollments", response_model=Enrollment, status_code=201)
def create_enrollment(data: EnrollmentIn) -> Enrollment:
    if course_by_id(data.course_id) is None:
        raise HTTPException(status_code=404, detail="Course not found")

    enrollment = Enrollment(
        id=len(ENROLLMENTS) + 1,
        course_id=data.course_id,
        student_name=data.student_name,
    )
    ENROLLMENTS.append(enrollment)
    return enrollment


@app.get("/enrollments", response_model=list[Enrollment])
def list_enrollments() -> list[Enrollment]:
    return ENROLLMENTS
