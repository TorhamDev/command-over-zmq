import asyncio
import zmq
import zmq.asyncio


context = zmq.asyncio.Context()


async def server():
    socket = context.socket(zmq.REP)
    socket.bind("tcp://*:5555")

    while True:
        #  Wait for next request from client
        message = await socket.recv()
        print("Received request: %s" % message)

        #  Send reply back to client
        await socket.send(b"World")


asyncio.run(server())
