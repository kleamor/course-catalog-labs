# Course Catalog API Lab 7

## Lab 8: GraphQL alongside REST

Install the updated requirements, then start the backend. The same PostgreSQL
database is available through REST at `/docs` and GraphQL at `/graphql`.
Opening `/graphql` in a browser shows GraphiQL. Example query:

```graphql
query MyCourses($id: ID!) {
  student(id: $id) {
    name
    enrollments { id course { title credits level } }
  }
}
```

Variables: `{ "id": "2" }`. The `enroll` and `likeCourse` mutations return
`userErrors` for expected application errors. REST uses Problem Details with
`application/problem+json` for the same errors. Both use the rules in
`services.py`.

DataLoaders batch nested student, course, and enrollment lookups. The
`X-SQL-Queries` response header shows the number of SQL statements; the
nested student query and the all-students query each make 3 SQL requests.
Depth and alias limits, bounded list arguments, error masking, and configurable
introspection protect the GraphQL endpoint. Set `GRAPHQL_INTROSPECTION=false`
in the local `.env` to disable schema discovery.

For the defense, run `python try_graphql.py`, `python try_n_plus_1.py`, and
`python measure.py` with the API server running. The frontend pages
`/my-courses` and `/my-courses-rest` show the same data via the two APIs.

From PowerShell in this backend folder, run the eight GraphQL self-checks:

```powershell
.\.venv\Scripts\python.exe try_graphql.py
```

Expected final line on the starting course data: `8 of 8 as expected`. The
checks cover a course list, one course, a missing course, a student's nested
courses, three expected enrollment errors, and a misspelled GraphQL field.

| Client view | HTTP requests | Typical SQL queries | Response size |
| --- | ---: | ---: | --- |
| REST My courses | 5 | 5 | Run `measure.py` for your current bytes |
| GraphQL My courses | 1 | 3 | Run `measure.py` for your current bytes |

On the local sample data, `measure.py` reported 1,956 response bytes and 226.9 ms
for REST versus 331 bytes and 11.2 ms for GraphQL. These are one-run measurements,
not a benchmark; repeat them on the defense machine.

Experiment observations: a misspelled GraphQL field produced `errors` with HTTP
200, while a missing REST course produced Problem Details with HTTP 404. A
student's three courses and all students' courses each took three SQL queries
with DataLoaders. A query deeper than five levels was rejected by the depth
limiter. A GET mutation was rejected with HTTP 400. Use `try_protection.py` for
more probes. `flood_likes.py` deliberately changes the database, so run it only
when you intend to demonstrate that behavior.

The timings and bytes depend on the machine and current data. The GraphQL
query includes only the fields requested by the page. A bad GraphQL field
returns an `errors` array, often with HTTP 200; clients must inspect it.
Expected rule errors are instead in the mutation's `userErrors`.

The backend now stores the course catalog in PostgreSQL. SQLAlchemy models describe the tables in Python, while Alembic keeps the database schema versioned.

## Start locally

1. Create a database and role as in Lab 6, then copy `.env.example` to `.env`.
2. Put your own local PostgreSQL password into `DATABASE_URL` in `.env`. Never commit this file.
3. Install and start the API:

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\alembic.exe upgrade head
.\.venv\Scripts\python.exe -m uvicorn main:app --reload
```

Open `http://127.0.0.1:8000/docs` to use Swagger UI.

## Database migration workflow

- `0001_create_catalog_tables` creates `courses`, `students`, and `enrollments`.
- `0002_add_course_level` adds a required `courses.level` column safely: it adds it nullable, fills existing rows with `beginner`, then makes it required.
- The existing Lab 6 database was marked at revision `0001` with `alembic stamp 0001`, then upgraded to `0002`. This avoids recreating or deleting existing data.

Useful commands:

```powershell
# Create a migration after changing a SQLAlchemy model
.\.venv\Scripts\alembic.exe revision --autogenerate -m "describe change"

# Inspect migration history and the active database revision
.\.venv\Scripts\alembic.exe current
.\.venv\Scripts\alembic.exe history

# Check model changes and apply migrations
.\.venv\Scripts\alembic.exe check
.\.venv\Scripts\alembic.exe upgrade head
.\.venv\Scripts\alembic.exe upgrade +1

# Undo the last migration if necessary
.\.venv\Scripts\alembic.exe downgrade -1

# Mark an existing database as a version without running that migration again
.\.venv\Scripts\alembic.exe stamp 0001

# Verify the project database and models
.\.venv\Scripts\python.exe check_db.py
.\.venv\Scripts\python.exe check_models.py
```

## Main API routes

- `GET /courses` filters, sorts, and paginates courses from PostgreSQL.
- `GET /courses/{course_id}` and `POST /courses/{course_id}/like` read and update a course.
- `POST /students` creates a student; duplicate email returns `409`.
- `POST /enrollments` links an existing student and course; foreign-key and duplicate errors become clear HTTP responses.
- `GET /enrollments` joins enrollment, course, and student data.
- `GET /stats/courses` uses `LEFT OUTER JOIN` and `COUNT` so courses without enrollments are included.

The API keeps camelCase JSON (`courseId`, `studentId`) at the browser boundary, but Python and database code use snake_case.

## Example: create a new migration

This is a learning example only. The current Lab 7 schema does not include `duration_hours`.

1. Add a nullable field to the `Course` model in `models.py`:

```python
duration_hours: Mapped[int] = mapped_column(nullable=True)
```

2. Generate a migration from the changed model:

```powershell
.\.venv\Scripts\alembic.exe revision --autogenerate -m "add course duration"
```

3. Review the new file in `alembic/versions/`. It should add the `duration_hours`
column to `courses`.

4. Apply it and verify the result:

```powershell
.\.venv\Scripts\alembic.exe upgrade head
.\.venv\Scripts\alembic.exe current
```

The expected current version after this example would be `0003 (head)`. To return
to the previous version, run `alembic downgrade -1` before removing the model field.

## Verification checklist for the defense

Start the API first, then run these commands from the `course-catalog-api-v2`
folder. They demonstrate more than eight independent checks.

```powershell
# 1. PostgreSQL connection, current database, and row counts
.\.venv\Scripts\python.exe check_db.py

# 2. ORM model columns, constraints, and indexes
.\.venv\Scripts\python.exe check_models.py

# 3. The migration revision applied to PostgreSQL
.\.venv\Scripts\alembic.exe current

# 4. SQLAlchemy models and Alembic migrations have no pending differences
.\.venv\Scripts\alembic.exe check

# 5-9. Invalid student (422), missing course (404), missing student (404),
# duplicate enrollment (409), and invalid pagination (422)
.\.venv\Scripts\python.exe try_errors.py

# 10. Automated API tests
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
```

The expected Alembic version is `0002 (head)`. The final automated test result
should be `OK`. The `try_errors.py` script requires the API at
`http://127.0.0.1:8000` to be running.

## Structure

- `config.py` reads the ignored `.env` settings.
- `db.py` owns the engine, sessions, metadata naming convention, and `get_db` dependency.
- `models.py` contains SQLAlchemy tables and relationships.
- `schemas.py` contains Pydantic validation and API response schemas.
- `alembic/versions/` contains reproducible schema migrations.
- `seed.sql`, `check_db.py`, `check_models.py`, and `try_errors.py` support setup and verification.
