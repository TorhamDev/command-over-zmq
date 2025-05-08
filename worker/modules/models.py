from pydantic import BaseModel


class CommandInput(BaseModel):
    command_type: str
    command_name: str
    parameters: list[str]
