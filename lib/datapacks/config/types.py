from typing import Any, final

from pydantic import BaseModel, StrictBool, StrictInt, StrictStr


class ConfigOptionBase(BaseModel, frozen=True):
    name: StrictStr
    # TODO: Replace `Any` w/ `TextComponent` once pydantic (v2) supports `NotRequired`.
    description: Any


class ServerConfigOptionBase(ConfigOptionBase):
    # Which target of the `pack.config` objective to store the option's value in.
    target: StrictStr


class PlayerConfigOptionBase(ConfigOptionBase):
    # The objective that stores the option's value for each player, and stores the
    #  current server default value in `$default`.
    objective: StrictStr


class BoolConfigOptionBase(ConfigOptionBase):
    default: StrictBool


class IntConfigOptionBase(ConfigOptionBase):
    # A string of the range of integers this option accepts (e.g. `"0..100"`, `"1.."`).
    accepts: StrictStr
    default: StrictInt


@final
class ConfigOptionChoice(ConfigOptionBase):
    default: StrictBool = False


class ChoiceConfigOptionBase(ConfigOptionBase):
    choices: list[ConfigOptionChoice]


@final
class ServerBoolConfigOption(BoolConfigOptionBase, ServerConfigOptionBase):
    pass


@final
class ServerIntConfigOption(IntConfigOptionBase, ServerConfigOptionBase):
    pass


@final
class ServerChoiceConfigOption(ChoiceConfigOptionBase, ServerConfigOptionBase):
    pass


ServerConfigOption = (
    ServerBoolConfigOption | ServerIntConfigOption | ServerChoiceConfigOption
)


@final
class PlayerBoolConfigOption(BoolConfigOptionBase, PlayerConfigOptionBase):
    pass


@final
class PlayerIntConfigOption(IntConfigOptionBase, PlayerConfigOptionBase):
    pass


@final
class PlayerChoiceConfigOption(ChoiceConfigOptionBase, PlayerConfigOptionBase):
    pass


PlayerConfigOption = (
    PlayerBoolConfigOption | PlayerIntConfigOption | PlayerChoiceConfigOption
)

ConfigOption = ServerConfigOption | PlayerConfigOption
