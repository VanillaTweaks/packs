from collections.abc import Callable
from typing import ParamSpec, TypeVar

from lib.datapacks.config.types import ConfigOption

ConfigOptionType = TypeVar("ConfigOptionType", bound=ConfigOption)
Params = ParamSpec("Params")


def adds_option(
    add_option: Callable[[ConfigOptionType], None],
    ConfigOptionClass: Callable[Params, ConfigOptionType],
):
    """Makes the decorated function construct the specified class from its arguments and
    pass the new instance of that class into the specified `add_option` callback.

    The decorated function should have no parameters or body, because this decorator
    automatically generates them for the function.
    """

    def decorator(_: Callable[[], None]) -> Callable[Params, None]:
        def decorated_function(*args: Params.args, **kwargs: Params.kwargs):
            option = ConfigOptionClass(*args, **kwargs)
            add_option(option)

        return decorated_function

    return decorator
