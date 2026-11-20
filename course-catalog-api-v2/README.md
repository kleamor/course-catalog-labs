# Course Catalog API Lab 7

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

## Structure

- `config.py` reads the ignored `.env` settings.
- `db.py` owns the engine, sessions, metadata naming convention, and `get_db` dependency.
- `models.py` contains SQLAlchemy tables and relationships.
- `schemas.py` contains Pydantic validation and API response schemas.
- `alembic/versions/` contains reproducible schema migrations.
- `seed.sql`, `check_db.py`, `check_models.py`, and `try_errors.py` support setup and verification.
