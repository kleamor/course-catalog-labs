import unittest

from fastapi.testclient import TestClient

from main import app


class CourseCatalogApiTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.client = TestClient(app)

    def test_root_and_database_course_list(self) -> None:
        self.assertEqual(self.client.get("/").json(), {"message": "Course Catalog API is running"})
        response = self.client.get("/courses?size=100")
        self.assertEqual(response.status_code, 200)
        self.assertGreaterEqual(len(response.json()), 1)
        self.assertIn("level", response.json()[0])
        self.assertIn("isElective", response.json()[0])

    def test_join_and_statistics_routes(self) -> None:
        enrollments = self.client.get("/enrollments")
        stats = self.client.get("/stats/courses")
        self.assertEqual(enrollments.status_code, 200)
        self.assertEqual(stats.status_code, 200)
        self.assertIn("courseId", stats.json()[0])
        self.assertIn("enrolled", stats.json()[0])

    def test_validation_and_not_found(self) -> None:
        self.assertEqual(self.client.get("/courses?page=0").status_code, 422)
        self.assertEqual(self.client.get("/courses/no-such-course").status_code, 404)
        response = self.client.post("/students", json={"name": "A", "email": "invalid"})
        self.assertEqual(response.status_code, 422)


if __name__ == "__main__":
    unittest.main()
