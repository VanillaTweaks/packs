from collections.abc import Callable
from typing import ParamSpec, TypeVar

from lib.datapacks.config.types import ConfigOption

ConfigOptionType = TypeVar("ConfigOptionType", bound=ConfigOption)
Params = ParamSpec("Params")


def appends_option(
    # The list which the decorated function should append options to.
    options: list[ConfigOptionType],
    # The class to construct from the decorated function's arguments and append to the
    #  specified list.
    ConfigOptionClass: Callable[Params, ConfigOptionType],
):
    """Makes the decorated function construct the specified class from its arguments and
    append the new instance of that class to the specified list.

    The decorated function should have no parameters or body, because this decorator
    automatically generates them for the function.
    """

    def decorator(_: Callable[[], None]) -> Callable[Params, None]:
        def decorated_function(*args: Params.args, **kwargs: Params.kwargs):
            option = ConfigOptionClass(*args, **kwargs)
            options.append(option)

        return decorated_function

    return decorator
