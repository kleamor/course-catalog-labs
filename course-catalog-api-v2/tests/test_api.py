import unittest

from fastapi.testclient import TestClient

from main import ENROLLMENTS, app
from course_queries import Page, filter_courses, paginate_courses, sort_courses
from data import COURSES


class CourseCatalogApiTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.client = TestClient(app)

    def course_ids(self, url: str) -> list[str]:
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200, response.text)
        return [course["id"] for course in response.json()]

    def setUp(self) -> None:
        ENROLLMENTS.clear()

    def test_root_reports_service_is_running(self) -> None:
        response = self.client.get("/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"message": "Course Catalog API is running"})

    def test_default_course_list_is_sorted_by_popularity(self) -> None:
        self.assertEqual(
            self.course_ids("/courses"),
            [
                "ai-integration",
                "modern-frontend",
                "web-security",
                "backend-fastapi",
                "databases-postgresql",
                "api-design",
            ],
        )

    def test_course_responses_are_camel_case_and_keep_snake_case_query_params(self) -> None:
        response = self.client.get("/courses")

        expected_fields = {
            "id",
            "title",
            "description",
            "credits",
            "isElective",
            "likes",
        }
        self.assertEqual(len(response.json()), 6)
        self.assertTrue(all(set(course) == expected_fields for course in response.json()))
        self.assertEqual(
            self.course_ids("/courses?is_elective=true"),
            ["ai-integration", "api-design"],
        )
        self.assertEqual(len(self.course_ids("/courses?isElective=true")), 6)

    def test_elective_filter_handles_true_and_false(self) -> None:
        self.assertEqual(
            self.course_ids("/courses?is_elective=true"),
            ["ai-integration", "api-design"],
        )
        self.assertEqual(
            self.course_ids("/courses?is_elective=false"),
            [
                "modern-frontend",
                "web-security",
                "backend-fastapi",
                "databases-postgresql",
            ],
        )

    def test_title_sort_is_alphabetical(self) -> None:
        self.assertEqual(
            self.course_ids("/courses?sort=title"),
            [
                "ai-integration",
                "api-design",
                "backend-fastapi",
                "modern-frontend",
                "databases-postgresql",
                "web-security",
            ],
        )

    def test_pagination_is_applied_after_sorting(self) -> None:
        self.assertEqual(
            self.course_ids("/courses?page=1&page_size=2"),
            ["ai-integration", "modern-frontend"],
        )
        self.assertEqual(
            self.course_ids("/courses?page=2&page_size=2"),
            ["web-security", "backend-fastapi"],
        )
        self.assertEqual(
            self.course_ids("/courses?page=3&page_size=2"),
            ["databases-postgresql", "api-design"],
        )
        self.assertEqual(self.course_ids("/courses?page=4&page_size=2"), [])

    def test_filter_sort_and_pagination_are_applied_in_order(self) -> None:
        self.assertEqual(
            self.course_ids(
                "/courses?is_elective=false&sort=title&page=2&page_size=2"
            ),
            ["databases-postgresql", "web-security"],
        )

    def test_single_course_and_not_found_response(self) -> None:
        found = self.client.get("/courses/web-security")
        missing = self.client.get("/courses/nope")

        self.assertEqual(found.status_code, 200)
        self.assertEqual(found.json()["id"], "web-security")
        self.assertEqual(missing.status_code, 404)
        self.assertEqual(missing.json(), {"detail": "Course not found"})

    def test_cors_allows_only_the_frontend_origin_and_preflight(self) -> None:
        allowed = self.client.get("/", headers={"Origin": "http://localhost:3000"})
        foreign = self.client.get("/", headers={"Origin": "http://evil.example"})
        preflight = self.client.options(
            "/enrollments",
            headers={
                "Origin": "http://localhost:3000",
                "Access-Control-Request-Method": "POST",
                "Access-Control-Request-Headers": "content-type",
            },
        )

        self.assertEqual(allowed.status_code, 200)
        self.assertEqual(
            allowed.headers.get("access-control-allow-origin"), "http://localhost:3000"
        )
        self.assertNotIn("access-control-allow-origin", foreign.headers)
        self.assertEqual(preflight.status_code, 200)
        self.assertEqual(
            preflight.headers.get("access-control-allow-origin"), "http://localhost:3000"
        )
        self.assertIn("POST", preflight.headers["access-control-allow-methods"])

    def test_like_returns_the_updated_course_and_not_found(self) -> None:
        before = self.client.get("/courses/web-security").json()["likes"]
        liked = self.client.post("/courses/web-security/like")
        missing = self.client.post("/courses/nope/like")

        self.assertEqual(liked.status_code, 200)
        self.assertEqual(liked.json()["likes"], before + 1)
        self.assertIn("isElective", liked.json())
        self.assertEqual(missing.status_code, 404)
        self.assertEqual(missing.json(), {"detail": "Course not found"})

    def test_enrollments_accept_camel_case_body_and_validate_it(self) -> None:
        created = self.client.post(
            "/enrollments",
            json={"courseId": "web-security", "studentName": "Aigerim"},
        )
        invalid_name = self.client.post(
            "/enrollments",
            json={"courseId": "web-security", "studentName": "A"},
        )
        missing_course = self.client.post(
            "/enrollments",
            json={"courseId": "nope", "studentName": "Aigerim"},
        )
        listed = self.client.get("/enrollments")

        self.assertEqual(created.status_code, 201)
        self.assertEqual(
            created.json(),
            {"courseId": "web-security", "studentName": "Aigerim", "id": 1},
        )
        self.assertEqual(invalid_name.status_code, 422)
        self.assertEqual(
            invalid_name.json()["detail"][0]["loc"], ["body", "studentName"]
        )
        self.assertEqual(missing_course.status_code, 404)
        self.assertEqual(missing_course.json(), {"detail": "Course not found"})
        self.assertEqual(listed.status_code, 200)
        self.assertEqual(listed.json(), [created.json()])

    def test_query_constraints_reject_invalid_values(self) -> None:
        for url in (
            "/courses?sort=banana",
            "/courses?page=0",
            "/courses?page_size=0",
            "/courses?page_size=101",
        ):
            with self.subTest(url=url):
                self.assertEqual(self.client.get(url).status_code, 422)

    def test_query_helpers_keep_the_filter_sort_page_pipeline_explicit(self) -> None:
        required_courses = filter_courses(list(COURSES), is_elective=False)
        alphabetical_courses = sort_courses(required_courses, "title")
        visible_courses = paginate_courses(alphabetical_courses, Page(offset=2, limit=2))

        self.assertEqual(
            [course.id for course in visible_courses],
            ["databases-postgresql", "web-security"],
        )

    def test_openapi_contains_six_operations_and_camel_case_schemas(self) -> None:
        schema = self.client.get("/openapi.json").json()
        operations = {
            (path, method)
            for path, path_item in schema["paths"].items()
            for method in path_item
        }

        self.assertEqual(
            operations,
            {
                ("/", "get"),
                ("/courses", "get"),
                ("/courses/{course_id}", "get"),
                ("/courses/{course_id}/like", "post"),
                ("/enrollments", "get"),
                ("/enrollments", "post"),
            },
        )
        course_schema = schema["components"]["schemas"]["Course"]
        self.assertEqual(
            set(course_schema["properties"]),
            {"id", "title", "description", "credits", "isElective", "likes"},
        )
        self.assertEqual(course_schema["properties"]["isElective"]["default"], False)
        self.assertEqual(course_schema["properties"]["likes"]["default"], 0)
        self.assertEqual(
            set(schema["components"]["schemas"]["EnrollmentIn"]["properties"]),
            {"courseId", "studentName"},
        )


if __name__ == "__main__":
    unittest.main()
