import asyncio
import json

import zmq
import zmq.asyncio
from modules.utils import run_os_command, validate_input

context = zmq.asyncio.Context()


async def server():
    socket = context.socket(zmq.REP)
    socket.bind("tcp://*:5555")

    while True:
        recved = await validate_input(await socket.recv())
        if type(recved) is tuple and recved[0] is False:
            response = {"status": "error", "errors": recved[1]}
            await socket.send(json.dumps(response).encode())
            continue

        excute_result = await run_os_command(
            command=recved.command_name, parameters=recved.parameters
        )
        response = {
            "status": "success",
            "command_type": recved.command_type,
            "given_command": recved.command_name,
            "result": excute_result["stdout"],
            "error": excute_result["stderr"],
        }
        await socket.send(json.dumps(response).encode())


asyncio.run(server())
