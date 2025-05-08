import asyncio
import subprocess
from typing import Tuple

from pydantic import ValidationError

from .models import CommandInput


def convert_errors(
    e: ValidationError,
) -> list[dict]:
    """
    Convering pydantic ValidationError errors to something readble for end user.
    Args:
        e: An error with type of ValidationError

    Returns:
        list[dict] readble error as list of dicts
    """
    errors: list[dict] = []
    for e in e.errors():
        error = {"Param": e["loc"][0], "Error": e["msg"], "Input": e["input"]}
        errors.append(error)
    return errors


def validate_input(data: str | bytes) -> Tuple[bool, list] | CommandInput:
    """
    Validate user input with pydanic model.

    Args:
        data: User input


    Returns:
        CommandInput: validated data in commandInput type as pydantid model
        Tuple[bool, list]: False and error list

    """
    try:
        commad = CommandInput.model_validate_json(data)
    except ValidationError as e:
        return False, convert_errors(e)

    return commad


async def run_os_command(command: str, parameters: list[str]) -> dict:
    """
    Runing command on runing os

    Args:
        command: the command you want to run e.g ls
        parameters: list of the command params e.g ['-a']


    Returns:
        dict: command result
        dict: respective erro in dict
    """
    full_command = [command] + parameters

    try:
        print(f"Executing: {' '.join(full_command)}")
        process = await asyncio.create_subprocess_exec(
            command,
            *parameters,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        stdout_bytes, stderr_bytes = await asyncio.wait_for(
            process.communicate(), timeout=10
        )
    except (FileNotFoundError, asyncio.TimeoutError) as e:
        if type(e) is FileNotFoundError:
            # Handle cases where the command itself is not found
            error_msg = f"command '{command}' not found."
            print(error_msg)
            return {
                "status": "error",
                "command": command,
                "parameters": parameters,
                "return_code": -1,
                "stdout": "",
                "stderr": error_msg,
            }
        elif type(e) is asyncio.TimeoutError:
            # do dont let user run commands that run forever!
            process.kill()
            await process.wait()
            return {
                "status": "error",
                "command": command,
                "parameters": parameters,
                "return_code": -1,
                "stdout": "",
                "stderr": "Command timed out.",
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
