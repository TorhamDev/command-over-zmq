import argparse
import asyncio
import json

import zmq
import zmq.asyncio
from modules.models import MultiCommands, SingleCommand
from modules.utils import display_result, read_commands_file
from rich import print

context = zmq.asyncio.Context()


async def client(file_path: str, address: str):
    """
    The command-over-zmq client, will handle seding commands and showing the response result.

    Args:
        file_path: the commands file path, have to be json file, can be a list or a single json data (read test.json)
        address: the command-over-zmq server address in tcp:// protocol e.g: tcp://localhost:5555

    """
    server_address = address
    commands = await read_commands_file(file_path=file_path)

    socket = context.socket(zmq.REQ)
    socket.connect(server_address)

    print(f"[green]Server:[/green] {server_address}")

    if type(commands) is SingleCommand:
        full_command = f"{commands.command_name} {' '.join(commands.parameters)}"
        print(f"[yellow]Sending commad: [/yellow] [blue]{full_command} {''}[/blue]")
        await socket.send(commands.model_dump_json().encode())
        res = json.loads(await socket.recv())
        await display_result(res)

    elif type(commands) is MultiCommands:
        for command in commands.command_list:
            full_command = f"{commands.command_name} {' '.join(commands.parameters)}"
            print(f"[yellow]Sending commad: [/yellow] [blue]{full_command} {''}[/blue]")
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


# TODO: error handling in loading command from file
