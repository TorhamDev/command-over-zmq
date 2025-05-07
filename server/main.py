import asyncio
import json

import zmq
import zmq.asyncio
from modules.utils import validate_input

context = zmq.asyncio.Context()


async def server():
    socket = context.socket(zmq.REP)
    socket.bind("tcp://*:5555")

    while True:
        recved = validate_input(await socket.recv())
        if type(recved) is tuple and recved[0] is False:
            response = {"status": "error", "errors": recved[1]}

        #  Send reply back to client
        await socket.send(json.dumps(response).encode())


asyncio.run(server())
