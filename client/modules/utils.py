import json

from aiofile import async_open
from modules.models import MultiCommands, SingleCommand


async def read_commands_file(file_path: str) -> MultiCommands | SingleCommand:
    # aiofile dosent do really Async it use threadpool.
    async with async_open(file_path, mode="r") as f:
        commands = await f.read()

    commands = json.loads(commands)

    if type(commands) is dict:
        return SingleCommand.model_validate(commands)

    return MultiCommands.model_validate({"command_list": commands})
