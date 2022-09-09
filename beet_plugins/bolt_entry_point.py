from beet import Context
from bolt import Module


def beet_default(ctx: Context):
    """Generates the Bolt module used by `lib:entry_point` to import everything in the
    pack.
    """

    ctx.data["pack"]["_entry_point"] = Module(
        "\n".join(
            # TODO: Remove import aliases.
            f"import {module} as _"
            for module, _ in ctx.data.content
            if module.startswith("pack:")
        )
    )
