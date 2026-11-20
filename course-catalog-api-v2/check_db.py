from sqlalchemy import text

from db import engine


with engine.connect() as connection:
    print("PostgreSQL:", connection.execute(text("select version()")).scalar_one())
    print("Current database:", connection.execute(text("select current_database()")).scalar_one())
    print("Courses:", connection.execute(text("select count(*) from courses")).scalar_one())
    print("Students:", connection.execute(text("select count(*) from students")).scalar_one())
    print("Enrollments:", connection.execute(text("select count(*) from enrollments")).scalar_one())
