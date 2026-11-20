"""Manual API checks for validation and database constraint errors.

Run the server first, then execute: python try_errors.py
"""

import httpx


base_url = "http://127.0.0.1:8000"
requests = [
    ("Invalid student", "POST", "/students", {"name": "A", "email": "bad"}),
    ("Unknown course", "POST", "/enrollments", {"courseId": "missing", "studentId": 1}),
    ("Unknown student", "POST", "/enrollments", {"courseId": "ai-integration", "studentId": 999999}),
    ("Duplicate enrollment", "POST", "/enrollments", {"courseId": "ai-integration", "studentId": 1}),
    ("Bad pagination", "GET", "/courses?page=0", None),
]

for title, method, path, payload in requests:
    response = httpx.request(method, f"{base_url}{path}", json=payload)
    print(title, response.status_code, response.json())
