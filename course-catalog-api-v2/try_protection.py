"""Probe GraphQL limits without changing data."""
import httpx

URL = "http://127.0.0.1:8000/graphql"
cases = {
    "too deep": '{ students { enrollments { course { enrollments { student { enrollments { id } } } } } } }',
    "too many aliases": '{ ' + ' '.join(f'a{i}: course(id: "api-design") {{ id }}' for i in range(11)) + ' }',
    "invalid limit": '{ courses(limit: 1000000) { id } }',
    "introspection": '{ __schema { queryType { name } } }',
}
for label, query in cases.items():
    response = httpx.post(URL, json={"query": query})
    body = response.json()
    print(label, response.status_code, body.get("errors", body.get("data")))
