from typing import Tuple

from pydantic import ValidationError

from .models import CommandInput


def convert_errors(
    e: ValidationError,
) -> list[str]:
    errors: list[dict] = []
    for e in e.errors():
        error = {"Param": e["loc"][0], "Error": e["msg"], "Input": e["input"]}
        errors.append(error)
    return errors


def validate_input(data: str | bytes) -> Tuple[bool, list] | CommandInput:
    try:
        commad = CommandInput.model_validate_json(data)
    except ValidationError as e:
        return False, convert_errors(e)

    return commad
