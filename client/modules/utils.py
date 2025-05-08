import json

from aiofile import async_open
from modules.models import MultiCommands, SingleCommand
from rich import print


async def read_commands_file(file_path: str) -> MultiCommands | SingleCommand:
    """
    Read and send commands from json file and recive its response.

    Args:
        file_path: commands json file path

    Returns:
        MultiCommands: if we have more than 1 command in json file
        SingleCommand: if only one command is in json file
    """
    # aiofile dosent do really Async it use threadpool.
    async with async_open(file_path, mode="r") as f:
        commands = await f.read()

    commands = json.loads(commands)

    if type(commands) is dict:
        return SingleCommand.model_validate(commands)

    return MultiCommands.model_validate({"command_list": commands})


async def display_result(result: dict) -> None:
    full_command = f"{result['given_command']} {' '.join(result['parameters'])}"
    if result["status"] == "success":
        print("[green]--------------- Successful ---------------[/green]")
        print(f"[yellow]Command:[/yellow] [bold]{full_command}[/bold]")
        print(f"[yellow]Type:[/yellow] {result['command_type']}")
        print(f"[yellow]Result:[/yellow]\n{result['result']}")
    elif result["status"] == "error":
        print("[red]--------------- Error ---------------[/red]")
        print(f"[yellow]Command:[/yellow] [bold]{full_command}[/bold]")
        print(f"[yellow]Type:[/yellow] {result['command_type']}")
        print(f"[red]Error[/red]: [bold]{result['error']}[/bold]")
