import asyncio

import zmq
import zmq.asyncio

context = zmq.asyncio.Context()

msg = """
{
    "command_type":"os",
    "command_name":"ls",
    "parameters": [
        "/home/torham/p/",
        "-a"
    ]


}


"""


async def client():
    print("Connecting to hello world server…")
    socket = context.socket(zmq.REQ)
    socket.connect("tcp://localhost:5555")

    await socket.send(msg.encode())
    res = await socket.recv()
    print(res)


asyncio.run(client())
