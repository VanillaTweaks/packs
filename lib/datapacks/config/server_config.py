from lib.datapacks.config.helpers import appends_option
from lib.datapacks.config.types import (
    ServerBoolConfigOption,
    ServerChoiceConfigOption,
    ServerConfigOption,
    ServerIntConfigOption,
)

options: list[ServerConfigOption] = []


@appends_option(options, ServerBoolConfigOption)
def add_bool_option():
    ...


@appends_option(options, ServerIntConfigOption)
def add_int_option():
    ...


@appends_option(options, ServerChoiceConfigOption)
def add_choice_option():
    ...
