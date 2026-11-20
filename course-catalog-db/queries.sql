-- queries.sql: SQL behind the Lab 5 API routes
-- Data-changing examples are rolled back, so this file is safe to re-run.

-- 1. GET /courses?is_elective=false&sort=popular&page=1&page_size=3
SELECT id, title, credits, likes
FROM courses
WHERE is_elective = false
ORDER BY likes DESC, id
LIMIT 3 OFFSET 0;

-- 1b. The same query, page 2.
SELECT id, title, credits, likes
FROM courses
WHERE is_elective = false
ORDER BY likes DESC, id
LIMIT 3 OFFSET 3;

-- 2. GET /courses/api-design
SELECT id, title, credits, is_elective, likes
FROM courses
WHERE id = 'api-design';

-- 2b. A missing course produces no rows; the API converts this to 404.
SELECT id, title, credits, is_elective, likes
FROM courses
WHERE id = 'no-such-course';

-- 3. POST /courses/api-design/like
BEGIN;
UPDATE courses
SET likes = likes + 1
WHERE id = 'api-design'
RETURNING id, likes;

-- 3b. A missing course updates zero rows; the API converts this to 404.
UPDATE courses
SET likes = likes + 1
WHERE id = 'no-such-course'
RETURNING id, likes;
ROLLBACK;

-- 4. POST /enrollments
BEGIN;
INSERT INTO enrollments (course_id, student_id)
VALUES ('web-security', 3)
RETURNING id, course_id, student_id;
ROLLBACK;

-- 5. GET /enrollments
SELECT e.id, s.name AS student, c.title AS course
FROM enrollments e
JOIN students s ON s.id = e.student_id
JOIN courses c ON c.id = e.course_id
ORDER BY e.id;

-- 6. Enrollment statistics, including courses with no enrollments.
SELECT c.id, count(e.id) AS enrolled
FROM courses c
LEFT JOIN enrollments e ON e.course_id = c.id
GROUP BY c.id
ORDER BY enrolled DESC, c.id;

-- 7. Courses without an enrollment.
SELECT c.id
FROM courses c
LEFT JOIN enrollments e ON e.course_id = c.id
WHERE e.id IS NULL
ORDER BY c.id;

-- 8. Students enrolled in more than one course.
SELECT s.name, count(*) AS courses
FROM students s
JOIN enrollments e ON e.student_id = s.id
GROUP BY s.id, s.name
HAVING count(*) > 1
ORDER BY courses DESC, s.name;
