from lib.datapacks.config.helpers import appends_option
from lib.datapacks.config.types import (
    PlayerBoolConfigOption,
    PlayerChoiceConfigOption,
    PlayerConfigOption,
    PlayerIntConfigOption,
)

options: list[PlayerConfigOption] = []


@appends_option(options, PlayerBoolConfigOption)
def add_bool_option():
    ...


@appends_option(options, PlayerIntConfigOption)
def add_int_option():
    ...


@appends_option(options, PlayerChoiceConfigOption)
def add_choice_option():
    ...
