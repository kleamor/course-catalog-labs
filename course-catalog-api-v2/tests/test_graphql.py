import unittest
from fastapi.testclient import TestClient
from main import app


class GraphQLTests(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

    def test_nested_student_courses(self):
        response = self.client.post("/graphql", json={"query": "{ student(id: \"2\") { name enrollments { course { id title } } } }"})
        self.assertEqual(response.status_code, 200)
        body = response.json()
        self.assertNotIn("errors", body)
        self.assertEqual(len(body["data"]["student"]["enrollments"]), 3)
        self.assertEqual(response.headers["X-SQL-Queries"], "3")

    def test_loader_batches_all_students(self):
        response = self.client.post("/graphql", json={"query": "{ students { enrollments { course { title } } } }"})
        self.assertNotIn("errors", response.json())
        self.assertEqual(response.headers["X-SQL-Queries"], "3")

    def test_expected_error_in_mutation(self):
        response = self.client.post("/graphql", json={"query": "mutation { enroll(input: {courseId: \"ai-integration\", studentId: \"3\"}) { enrollment { id } userErrors { code } } }"})
        self.assertEqual(response.json()["data"]["enroll"]["userErrors"][0]["code"], "ALREADY_ENROLLED")

    def test_rest_problem(self):
        response = self.client.get("/courses/nope")
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.headers["content-type"], "application/problem+json")

    def test_protection_and_get_mutation(self):
        nested = "{ students { enrollments { course { enrollments { student { enrollments { id } } } } } } }"
        response = self.client.post("/graphql", json={"query": nested})
        self.assertIn("errors", response.json())
        response = self.client.get("/graphql", params={"query": 'mutation { likeCourse(id: "api-design") { course { likes } } }'}, headers={"Accept": "application/json"})
        self.assertEqual(response.status_code, 400)
