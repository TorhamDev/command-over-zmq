import argparse
import asyncio

import zmq
import zmq.asyncio
from modules.models import MultiCommands, SingleCommand
from modules.utils import read_commands_file

context = zmq.asyncio.Context()


async def client(file_path: str):
    server_address = "tcp://localhost:5555"
    print(f"Loading {file_path}")
    commands = await read_commands_file(file_path=file_path)

    socket = context.socket(zmq.REQ)
    socket.connect(server_address)
    print(f"Connected to {server_address}")

    if type(commands) is SingleCommand:
        await socket.send(commands.model_dump_json().encode())
        res = await socket.recv()
        print(res)

    elif type(commands) is MultiCommands:
        for command in commands.command_list:
            await socket.send(command.model_dump_json().encode())
            res = await socket.recv()
            print(res)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="command over zmq client",
        description="Help you to communicate with the zmq command server",
    )

    parser.add_argument(
        "-f", "--file", help="Json commands file address", required=True
    )
    args = parser.parse_args()

    asyncio.run(client(file_path=args.file))


# TODO: Read command from file
# TODO: add rich lib and make output better
# TODO: Allow multi command excute
