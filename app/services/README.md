# services

Package for CRUDs and mixins

## CRUDs

Each new CRUD must be inherited from `Base`

### You must define for new CRUD

* `model` - class field with ORM class which CRUD will be use

### Optional fields for defining

* `columns_to_update` - list of columns of ORM that can be updated, for example
  ```python
  columns_to_update = [UserORM.name, UserORM.surname, UserORM.avatar]
  ```
* `simple_columns_to_update` - list of columns of ORM that can be updated by simple assignment

### Optional methods for defining

* `_before_create` - method that called before creation new row in database, it can be used for checking unique fields or existing rows
* `_update_complicated_columns` - method that called for updating row in database, it can be used for updating of columns, values of which depends on some conditions
* `_before_delete` - method that called before deletion existing row in database, it can be used for deletion rows in other services
* `init` - method that can be called on application startup, it can be used for database initialization

### commit and refresh

CRUD `Base` contains method `commit` for transaction commit and method `refresh` for updating ORM instance after commit

You can call `refresh` only for objects that have been creating or updating, because you can't update ORM instance if row doesn't exist in database - it will raise an exception

It is recommended to call `commit` only in API requests functions or in the end of Celery tasks for atomicity of all changes
