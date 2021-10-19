# routers

Package for REST API routers

## Commit exceptions

If the commit fails, an exception is thrown that you must catch

### Methods to define specific cause of exception

There are some methods below to define specific cause of exception and you can use any of them

1. `pgcode` using

    ```python
    from psycopg2 import Error as PSQLError
    from psycopg2.errorcodes import UNIQUE_VIOLATION
    from sqlalchemy.exc import IntegrityError
    ...
    def some_route(db: Session = Depends(get_db)):
        ...
        try:
            SomeCRUD.commit(db)
        except IntegrityError as e:
            orig: PSQLError = e.orig
            if orig.pgcode == UNIQUE_VIOLATION:
                raise HTTPException(status.HTTP_403_FORBIDDEN, orig.diag.message_detail)
            ...
        ...
    ```

2. Specific error class using

    ```python
    from psycopg2.errors import lookup
    from psycopg2.errorcodes import UNIQUE_VIOLATION
    from sqlalchemy.exc import IntegrityError
    ...
    UniqueViolation = lookup(UNIQUE_VIOLATION)
    ...
    def some_route(db: Session = Depends(get_db)):
        ...
        try:
            SomeCRUD.commit(db)
        except IntegrityError as e:
            if isinstance(e.orig, UniqueViolation):
                raise HTTPException(status.HTTP_403_FORBIDDEN, e.orig.diag.message_detail)
            ...
        ...
    ```

### List of exceptions

Each exception inherited from `SQLAlchemyError` equal to set of PostgreSQL exceptions

We must define specific PostgreSQL exception when we expect more than one exception from set of PostgreSQL exceptions, because we do a lot of checks in Python code for successful transaction

When you think about specific exceptions, think "what if two transactions will update these rows" and other cases

[Full list of PostgreSQL exceptions](https://www.psycopg.org/docs/errors.html)

There is list of possible exceptions (and their meaning) in our application bellow

* `sqlalchemy.exc.IntegrityError`
  - unique constraint violated (`psycopg2.errors.UniqueViolation`)
* `sqlalchemy.exc.OperationalError`
  - couldn't connect to database (`psycopg2.OperationalError`)

If you find specific exception that doesn't exist in list above then please append this to the list
