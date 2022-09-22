from lib.types import Function, FunctionType

functions_to_run_last: list[Function] = []


def run_last(function: FunctionType) -> FunctionType:
    """Runs the decorated function after the rest of the pack's modules finish
    running.
    """

    functions_to_run_last.append(function)

    return function


def run_last_functions():
    """Runs all of the functions decorated by `run_last`."""

    for function in functions_to_run_last:
        function()
