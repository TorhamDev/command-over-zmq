import asyncio
import json

import zmq
import zmq.asyncio
from modules.utils import run_os_command, validate_input

context = zmq.asyncio.Context()


async def server():
    socket = context.socket(zmq.REP)
    socket.connect("tcp://localhost:8888")

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
            "status": excute_result["status"],
            "command_type": recved.command_type,
            "given_command": recved.command_name,
            "parameters": excute_result["parameters"],
            "result": excute_result["stdout"],
            "error": excute_result["stderr"],
        }
        await socket.send(json.dumps(response).encode())


async def broker():
    frontend = context.socket(zmq.ROUTER)
    frontend.bind("tcp://*:8000")

    backend = context.socket(zmq.DEALER)
    backend.bind("tcp://*:8888")

    poller = zmq.asyncio.Poller()
    poller.register(frontend, zmq.POLLIN)
    poller.register(backend, zmq.POLLIN)

    while True:
        events = dict(await poller.poll())

        print(events.items())

        if frontend in events:
            msg = await frontend.recv_multipart()
            await backend.send_multipart(msg)

        if backend in events:
            msg = await backend.recv_multipart()
            await frontend.send_multipart(msg)


async def main():
    # Launch broker once
    broker_task = asyncio.create_task(broker())

    # Launch multiple independent workers
    worker_tasks = [
        asyncio.create_task(server())
        for _ in range(5)  # You can tune this number
    ]

    await asyncio.gather(broker_task, *worker_tasks)


asyncio.run(main())

# TODO: add whitelist
# TODO: add test
