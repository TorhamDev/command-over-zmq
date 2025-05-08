import asyncio
import subprocess
from typing import Tuple

from pydantic import ValidationError

from .models import CommandInput


async def convert_errors(
    e: ValidationError,
) -> list[str]:
    errors: list[dict] = []
    for e in e.errors():
        error = {"Param": e["loc"][0], "Error": e["msg"], "Input": e["input"]}
        errors.append(error)
    return errors


async def validate_input(data: str | bytes) -> Tuple[bool, list] | CommandInput:
    try:
        commad = CommandInput.model_validate_json(data)
    except ValidationError as e:
        return False, await convert_errors(e)

    return commad


async def run_os_command(command: str, parameters: list[str]) -> dict:
    full_command = [command] + parameters

    try:
        print(f"Executing: {' '.join(full_command)}")
        process = await asyncio.create_subprocess_exec(
            command,
            *parameters,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        stdout_bytes, stderr_bytes = await process.communicate()
    except FileNotFoundError:
        # Handle cases where the command itself is not found
        error_msg = f"command '{command}' not found."
        print(error_msg)
        return {
            "status": "error",
            "command": command,
            "parameters": parameters,
            "stdout": "",
            "stderr": error_msg,
        }

    stdout = stdout_bytes.decode().strip()
    stderr = stderr_bytes.decode().strip()

    returncode = process.returncode

    command_result = {
        "status": "success",
        "command": command,
        "parameters": parameters,
        "return_code": returncode,
        "stdout": stdout,
        "stderr": stderr,
    }

    return command_result
