# mq

Package for RPC

## Connection

Class that contains only `connection` and `channel` for connection with RabbitMQ

Each worker has only one connection and channel

Connection is opened on the startup event and closed on shutdown event of the FastAPI application

## RPC

Client and server classes for RPC pattern simply based on the [RPC pattern of aio-pika](https://github.com/mosquito/aio-pika/blob/master/aio_pika/patterns/rpc.py) ([docs](https://aio-pika.readthedocs.io/en/latest/patterns.html#rpc))

You can read about this pattern [here](https://www.rabbitmq.com/tutorials/tutorial-six-python.html)

For each service we have one queue for incoming messages

If you want to use unique queue for each worker, then set `BROKER_CLIENT_QUEUE` to `null` by `*.env` file 

RPC server starts consuming messages on the startup event of the FastAPI application

Example of RPC client in CRUD:
```python
from pydantic import ValidationError

from .base import Base, Session
from ...exceptions import DeletionRemoteError, ServiceDeliveryError, ServiceResponseError
from ...models import ExampleORM
from ...mq import someClient, DeleteExampleRequest, DeleteModelResponse, DeliveryError


class Example(Base):
    model = ExampleORM

    ...

    @classmethod
    async def delete_remote_example(cls, example_id: int):
        try:
            body = DeleteExampleRequest(example_id=example_id)
            response = await someClient.call(body, DeleteModelResponse)
        except DeliveryError:
            raise ServiceDeliveryError(f"Example {example_id} can't be deleted due to troubles with services connection")
        except ValidationError:
            raise ServiceResponseError(f"Example {example_id} can't be deleted due to service response misunderstanding")
        if not response.success:
            raise DeletionRemoteError(f"Example {example_id} can't be deleted due to error on another service")

    @classmethod
    async def _before_delete(cls, example: ExampleORM):
        await cls.delete_remote_example(example.example_id)
```
