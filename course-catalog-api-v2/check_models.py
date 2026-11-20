from sqlalchemy import inspect

from db import engine
from models import Course, Enrollment, Student


def table_summary(model: type[Course] | type[Student] | type[Enrollment]) -> None:
    table = model.__table__
    print(f"\n{table.name}")
    print("columns:", [column.name for column in table.columns])
    print("constraints:", sorted(constraint.name for constraint in table.constraints if constraint.name))
    print("indexes:", sorted(index.name for index in table.indexes))


for mapped_model in (Course, Student, Enrollment):
    table_summary(mapped_model)

inspector = inspect(engine)
print("\nDatabase tables:", inspector.get_table_names())
