import asyncio
import zmq
import zmq.asyncio


context = zmq.asyncio.Context()

msg = input("Enter msg: ")

async def client():
    print("Connecting to hello world server…")
    socket = context.socket(zmq.REQ)
    socket.connect("tcp://localhost:5555")

    for request in range(10):
        print("Sending request %s …" % request)
        await socket.send(msg.encode())

        #  Get the reply.
        message = await socket.recv()
        print("Received reply %s [ %s ]" % (request, message))


asyncio.run(client())
