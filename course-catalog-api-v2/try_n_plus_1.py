"""Show that nested relations are fetched in batches."""
import httpx

URL = "http://localhost:8000/graphql"
cases = [
    ("student 2", '{ student(id: "2") { enrollments { course { title } } } }'),
    ("all students", '{ students { enrollments { course { title } } } }'),
]
for label, query in cases:
    response = httpx.post(URL, json={"query": query})
    body = response.json()
    print(label, "SQL queries:", response.headers.get("X-SQL-Queries"), "errors:", body.get("errors"))
