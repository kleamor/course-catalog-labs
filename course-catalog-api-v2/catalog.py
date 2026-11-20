"""Read-only access to the in-memory course catalog."""

from data import COURSES
from models import Course


def all_courses() -> list[Course]:
    """Return a fresh list so callers cannot rearrange the catalog itself."""
    return list(COURSES)


def course_by_id(course_id: str) -> Course | None:
    """Find one course by its public identifier."""
    return next((course for course in COURSES if course.id == course_id), None)
