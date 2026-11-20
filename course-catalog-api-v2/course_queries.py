"""Pure query helpers for the course-list endpoint."""

from dataclasses import dataclass
from typing import Literal

from fastapi import Query

from models import Course


SortOrder = Literal["popular", "title"]


@dataclass(frozen=True)
class Page:
    """A validated slice of a result collection."""

    offset: int
    limit: int


def pagination(
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=20, ge=1, le=100),
) -> Page:
    """Translate public page controls into a list slice."""
    return Page(offset=(page - 1) * page_size, limit=page_size)


def filter_courses(courses: list[Course], is_elective: bool | None) -> list[Course]:
    if is_elective is None:
        return courses
    return [course for course in courses if course.is_elective == is_elective]


def sort_courses(courses: list[Course], sort: SortOrder) -> list[Course]:
    if sort == "title":
        return sorted(courses, key=lambda course: course.title)
    return sorted(courses, key=lambda course: course.likes, reverse=True)


def paginate_courses(courses: list[Course], page: Page) -> list[Course]:
    return courses[page.offset : page.offset + page.limit]
