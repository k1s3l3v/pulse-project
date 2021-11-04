from .client import DeliveryError, RPCClient
from .connection import Connection
from .methods import delete_project
from .schemas import *
from .server import RPCServer
from ..config import settings


staffClient = RPCClient(settings.STAFF_BROKER_SERVICE_QUEUE)
pulseServer = RPCServer(settings.BROKER_SERVICE_QUEUE)

pulseServer.register_procedure(DeleteProjectRequest, delete_project, DeleteModelResponse)
