import asyncio
from typing import (
    List,
)

import zmq
import zmq.asyncio
from pydantic import BaseModel

context = zmq.asyncio.Context()


class CommandInput(BaseModel):
    command_type: str
    command_name: str
    parameters: List[str]


async def server():
    socket = context.socket(zmq.REP)
    socket.bind("tcp://*:5555")

    while True:
        #  Wait for next request from client
        message = CommandInput.model_validate_json(await socket.recv())
        print(message)

        #  Send reply back to client
        await socket.send(b"World")


asyncio.run(server())
