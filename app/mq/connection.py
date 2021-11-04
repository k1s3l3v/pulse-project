from aio_pika import connect_robust, RobustChannel, RobustConnection
from asyncio import AbstractEventLoop

from ..config import settings
from ..utils import Singleton


class Connection(metaclass=Singleton):
    channel: RobustChannel
    connection: RobustConnection

    async def open(self, loop: AbstractEventLoop):
        if hasattr(self, 'connection') and not self.connection.is_closed:
            return
        self.connection = await connect_robust(host=settings.BROKER_HOST, port=settings.BROKER_PORT, loop=loop,
                                               login=settings.BROKER_LOGIN, password=settings.BROKER_PASSWORD)
        self.channel = await self.connection.channel()
        await self.channel.set_qos(1)

    async def close(self):
        if not hasattr(self, 'connection') or self.connection.is_closed:
            return
        await self.channel.close()
        await self.connection.close()
