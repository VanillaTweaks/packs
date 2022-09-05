from typing import Any

from beet import Context
from mecha import AstJson, AstJsonValue


def get_custom_json_values(ctx: Context):
    """Calls the `_get_ast_json_value_` method of any object in resource JSON and uses
    the returned value in its place in the compiled JSON.
    """

    initial_from_value = AstJson.from_value

    def from_value(value: Any) -> AstJson:
        if hasattr(value, "_get_ast_json_value_"):
            return AstJsonValue(value=value._get_ast_json_value_())
        else:
            return initial_from_value(value)

    AstJson.from_value = from_value
