import json

from aio_pika.message import IncomingMessage, Message
from pydantic import ValidationError
from typing import Callable, Dict, Type, TypeVar

from .connection import Connection
from .schemas import Request, Response
from ..schemas import BaseModel


_RequestT = TypeVar('_RequestT', bound=Request)
_ResponseT = TypeVar('_ResponseT', bound=Response)


class _Procedure(BaseModel):
    request_model: Type[Request]
    method: Callable[[_RequestT], _ResponseT]
    response_model: Type[Response]


class RPCServer:
    _procedures: Dict[str, _Procedure]

    def __init__(self, consume_queue: str):
        self._connection = Connection()
        self._consume_queue = consume_queue
        self._procedures = dict()

    def register_procedure(self, request_model: Type[Request], method: Callable[[_RequestT], _ResponseT],
                           response_model: Type[Response]):
        self._procedures[request_model.__fields__['type'].default] = _Procedure(**locals())

    async def _process_request(self, message: IncomingMessage):
        body = json.loads(message.body)
        if isinstance(body, dict) and 'type' in body and body['type'] in self._procedures:
            procedure = self._procedures[body['type']]
            try:
                response = procedure.method(procedure.request_model(**body))
            except ValidationError:
                response = procedure.response_model()
            response_message = Message(response.json().encode(), delivery_mode=message.delivery_mode,
                                       correlation_id=message.correlation_id)
            await self._connection.channel.default_exchange.publish(response_message, message.reply_to, mandatory=False)
            await message.ack()
        else:
            await message.reject(True)

    async def consume(self):
        queue = await self._connection.channel.declare_queue(self._consume_queue)
        await queue.consume(self._process_request)
