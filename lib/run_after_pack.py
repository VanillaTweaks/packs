from collections.abc import Callable
from typing import TypeVar

from lib.types import Unknown

FunctionType = TypeVar("FunctionType", bound=Callable[..., Unknown])

functions_to_run_last: list[Callable[..., Unknown]]


def run_last(function: FunctionType) -> FunctionType:
    """Runs the decorated function after the rest of the pack's modules finish
    running.
    """

    functions_to_run_last.append(function)

    return function
