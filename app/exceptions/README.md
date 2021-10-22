# exceptions

Package for exceptions

In order to make the code clearer and not contain many similar checks, which increases the code volume, it was decided to raise an exception at the first unsuccessful check of a certain condition

All these exceptions (and handlers for it) are described here

You can write your own exception about specific model absence, for example
```python
class ExampleNotFoundError(ModelNotFoundError):
    def __init__(self, example_id: int):
        super().__init__(f'Example {example_id} not found')
```
