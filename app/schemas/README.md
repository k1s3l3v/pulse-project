# schemas

Package for pydantic schemas for REST API (only for body)

Each new schema for input data must be inherited from `TrimModel`

Use `Field` for write description and some limitations for field

If you write schema for output data and want use ORM instances you must write `orm_mode = True` in the schema configuration class, for example
```python
class User(TrimModel):
    user_id: int = Field(..., description='The user unique identifier', gt=0)
    name: str = Field(..., description='The user name')
    surname: str = Field(..., description='The user surname')
    avatar: str = Field(..., description='The user avatar')

    class Config(TrimModel.Config):
        orm_mode = True
```
