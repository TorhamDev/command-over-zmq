from pydantic import BaseModel


class SingleCommand(BaseModel):
    command_type: str
    command_name: str
    parameters: list[str]


class MultiCommands(BaseModel):
    command_list: list[SingleCommand]
