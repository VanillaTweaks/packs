from beet import Context
from bolt import Runtime

from bolt.helpers import converter
from mecha import AstJson, AstJsonValue

from typing import Any
from dataclasses import dataclass


@dataclass(frozen=True)
class AstJsonCustomValue(AstJson):
    @classmethod
    def from_value(cls, value: Any) -> AstJson:
        if hasattr(value, "_get_ast_json_value_"):
            return AstJsonValue(value=value._get_ast_json_value_())
        else:
            return AstJson.from_value(value)


def get_custom_json_values(ctx: Context):
    """Calls the `_get_ast_json_value_` method of any object in resource JSON and uses
    the returned value in its place in the compiled JSON.
    """

    ctx.inject(Runtime).helpers["get_custom_json_values"] = converter(AstJsonCustomValue.from_value)
