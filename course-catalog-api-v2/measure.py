"""Measure the requests used to display student 2's courses."""
import json
import time
import httpx

BASE = "http://127.0.0.1:8000"

def request(client, method, path, **kwargs):
    response = client.request(method, path, **kwargs)
    response.raise_for_status()
    return response

with httpx.Client(base_url=BASE) as client:
    started = time.perf_counter()
    rest = [request(client, "GET", "/students"), request(client, "GET", "/enrollments")]
    mine = [item for item in rest[1].json() if item["studentId"] == 2]
    rest += [request(client, "GET", f'/courses/{item["courseId"]}') for item in mine]
    rest_ms = round((time.perf_counter() - started) * 1000, 1)

    started = time.perf_counter()
    graphql = request(client, "POST", "/graphql", json={"query": 'query MyCourses($id: ID!) { student(id: $id) { name enrollments { id course { title credits level } } } }', "variables": {"id": "2"}})
    graphql_ms = round((time.perf_counter() - started) * 1000, 1)
    if graphql.json().get("errors"):
        raise RuntimeError(graphql.json()["errors"])

    for label, responses, elapsed in [("REST", rest, rest_ms), ("GraphQL", [graphql], graphql_ms)]:
        print(label, json.dumps({"requests": len(responses), "bytes": sum(len(r.content) for r in responses), "sql": sum(int(r.headers.get("X-SQL-Queries", 0)) for r in responses), "elapsed_ms": elapsed}))
