import json

from aio_pika.exceptions import DeliveryError
from aio_pika.message import IncomingMessage, Message, ReturnedMessage
from aio_pika.queue import Queue
from asyncio import AbstractEventLoop, Future
from time import sleep
from typing import Dict, Optional, Type

from .connection import Connection
from .schemas import Request, Response
from ..config import settings


class RPCClient:
    _callback_queue: Queue
    _futures: Dict[int, Future]
    _loop: AbstractEventLoop

    def __init__(self, publish_queue: str):
        self._connection = Connection()
        self._futures = dict()
        self._publish_queue = publish_queue

    async def init(self, loop: AbstractEventLoop):
        self._loop = loop
        auto_delete = settings.BROKER_CLIENT_QUEUE is None
        self._callback_queue = await self._connection.channel.declare_queue(settings.BROKER_CLIENT_QUEUE,
                                                                            auto_delete=auto_delete)
        await self._callback_queue.consume(self._process_response)
        self._connection.channel.add_close_callback(self._process_close)
        self._connection.channel.add_on_return_callback(self._process_returned_message)  # type: ignore

    def _remove_future(self, future: Future):
        self._futures.pop(id(future), None)

    def _create_future(self) -> Future:
        future = self._loop.create_future()
        self._futures[id(future)] = future
        future.add_done_callback(self._remove_future)
        return future

    def _process_close(self, sender: 'RPCClient', exc: Optional[BaseException] = None):
        for future in self._futures.values():
            if future.done():
                continue
            future.set_exception(exc or Exception)

    def _process_returned_message(self, sender: 'RPCClient', message: ReturnedMessage):
        correlation_id = int(message.correlation_id) if message.correlation_id else None
        future = self._futures.pop(correlation_id, None)
        if future is not None and not future.done():
            future.set_exception(DeliveryError(message, None))  # type: ignore

    async def _process_response(self, message: IncomingMessage):
        correlation_id = int(message.correlation_id) if message.correlation_id else None
        future = self._futures.pop(correlation_id, None)
        if future is not None:
            future.set_result(json.loads(message.body))
            await message.ack()
        else:
            await message.reject(True)

    async def call(self, body: Request, response_model: Type[Response]) -> Response:
        future = self._create_future()
        message = Message(body.json().encode(), correlation_id=id(future), reply_to=self._callback_queue.name)
        try:
            await self._connection.channel.default_exchange.publish(message, self._publish_queue, mandatory=True)
            response = await future
        except RuntimeError:
            while not future.done():
                sleep(0.05)
            exception = future.exception()
            if exception is not None:
                raise exception
            response = future.result()
        return response_model(**response)
