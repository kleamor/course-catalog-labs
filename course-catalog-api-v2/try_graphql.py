"""Eight read-only or expected-error GraphQL checks from Lab 8."""
import httpx

URL = "http://127.0.0.1:8000/graphql"


def enroll(course_id: str, student_id: str) -> str:
    return (
        "mutation { enroll(input: "
        f'{{courseId: "{course_id}", studentId: "{student_id}"}}) '
        "{ enrollment { id } userErrors { code } } }"
    )


def first_error(data: dict) -> str:
    return data["errors"][0]["message"].split(". Did you")[0]


# Each case checks the answer, not only HTTP 200: GraphQL can return errors with 200.
CASES = [
    ("courses(limit: 2)", "{ courses(limit: 2) { id } }",
     lambda d: ",".join(c["id"] for c in d["data"]["courses"]),
     "ai-integration,modern-frontend"),
    ('course(id: "api-design")', '{ course(id: "api-design") { title } }',
     lambda d: d["data"]["course"]["title"], "API Design: REST vs GraphQL"),
    ('course(id: "nope")', '{ course(id: "nope") { title } }',
     lambda d: str(d["data"]["course"]), "None"),
    ("student(id: 2) -> courses", '{ student(id: "2") { enrollments { course { id } } } }',
     lambda d: str(len(d["data"]["student"]["enrollments"])), "3"),
    ("enroll twice", enroll("ai-integration", "3"),
     lambda d: d["data"]["enroll"]["userErrors"][0]["code"], "ALREADY_ENROLLED"),
    ("enroll: unknown course", enroll("nope", "3"),
     lambda d: d["data"]["enroll"]["userErrors"][0]["code"], "COURSE_NOT_FOUND"),
    ("enroll: unknown student", enroll("web-security", "999"),
     lambda d: d["data"]["enroll"]["userErrors"][0]["code"], "STUDENT_NOT_FOUND"),
    ("unknown field", '{ course(id: "api-design") { titel } }',
     first_error, "Cannot query field 'titel' on type 'Course'"),
]


def main() -> None:
    passed = 0
    with httpx.Client(timeout=10) as client:
        for title, query, pick, expected in CASES:
            response = client.post(URL, json={"query": query})
            try:
                actual = pick(response.json())
            except (KeyError, IndexError, TypeError, ValueError):
                actual = "?"
            ok = response.status_code == 200 and actual == expected
            passed += ok
            print(f"{'ok  ' if ok else 'FAIL'} {title:<25} {actual}")
    print(f"{passed} of {len(CASES)} as expected")


if __name__ == "__main__":
    main()
