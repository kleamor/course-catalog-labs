# Course Catalog Labs

This repository contains the complete Course Catalog coursework.

- `course-catalog-v2` - Next.js frontend from Lab 5.
- `course-catalog-api-v2` - FastAPI backend from Labs 5 and 7, now using PostgreSQL, SQLAlchemy, and Alembic.
- `course-catalog-db` - PostgreSQL schema, seed data, SQL queries, and database experiments from Lab 6.

## Run Lab 5

Start the API in `course-catalog-api-v2`, then start the frontend in
`course-catalog-v2`. The application uses `http://localhost:8000` for the API
and `http://localhost:3000` for the frontend.

## Run Lab 6

See `course-catalog-db/README.md` for the PostgreSQL role, database setup, and
commands for loading the schema, seed data, and queries.

## Run Lab 7

See `course-catalog-api-v2/README.md`. Create a local `.env` from
`.env.example`, install the Python requirements, then run `alembic upgrade head`
before starting FastAPI. The `.env` file is intentionally excluded from Git.
