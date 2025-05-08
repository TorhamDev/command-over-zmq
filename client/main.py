import argparse
import asyncio
import json

import zmq
import zmq.asyncio
from modules.models import MultiCommands, SingleCommand
from modules.utils import display_result, read_commands_file

context = zmq.asyncio.Context()


async def client(file_path: str, address: str):
    server_address = address
    print(f"Loading {file_path}")
    commands = await read_commands_file(file_path=file_path)

    socket = context.socket(zmq.REQ)
    socket.connect(server_address)

    print(f"Target Server: {server_address}")

    if type(commands) is SingleCommand:
        await socket.send(commands.model_dump_json().encode())
        res = json.loads(await socket.recv())
        await display_result(res)

    elif type(commands) is MultiCommands:
        for command in commands.command_list:
            await socket.send(command.model_dump_json().encode())
            res = json.loads(await socket.recv())
            await display_result(res)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="command over zmq client",
        description="Help you to communicate with the zmq command server",
    )

    parser.add_argument(
        "-f", "--file", help="Json commands file address", required=True
    )

    parser.add_argument(
        "-a",
        "--address",
        help="Server Address in TCP e.g: tcp://localhost:5555",
        required=True,
    )
    args = parser.parse_args()

    asyncio.run(client(file_path=args.file, address=args.address))


# TODO: Read command from file
# TODO: add rich lib and make output better
# TODO: Allow multi command excute
