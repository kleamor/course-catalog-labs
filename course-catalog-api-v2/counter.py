"""Count SQL statements for each HTTP request."""
from contextvars import ContextVar
from sqlalchemy import event
from db import engine

_counter: ContextVar[list[int] | None] = ContextVar("sql_counter", default=None)

@event.listens_for(engine, "before_cursor_execute")
def count_query(conn, cursor, statement, parameters, context, executemany):
    value = _counter.get()
    if value is not None:
        value[0] += 1

async def sql_query_header(request, call_next):
    value = [0]
    token = _counter.set(value)
    try:
        response = await call_next(request)
        response.headers["X-SQL-Queries"] = str(value[0])
        return response
    finally:
        _counter.reset(token)
