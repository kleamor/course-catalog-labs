import httpx

URL = "http://127.0.0.1:8000/graphql"
CASES = [
    ("course fields", '{ courses(limit: 2) { id title level } }', lambda d: len(d["data"]["courses"]) == 2),
    ("nested student", '{ student(id: "2") { enrollments { course { id } } } }', lambda d: len(d["data"]["student"]["enrollments"]) == 3),
    ("duplicate enrollment", 'mutation { enroll(input: {courseId: "ai-integration", studentId: "3"}) { userErrors { code } } }', lambda d: d["data"]["enroll"]["userErrors"][0]["code"] == "ALREADY_ENROLLED"),
    ("unknown field", '{ course(id: "api-design") { titel } }', lambda d: "errors" in d),
]
for label, query, check in CASES:
    response = httpx.post(URL, json={"query": query})
    print(label, "OK" if response.status_code == 200 and check(response.json()) else "FAIL")
