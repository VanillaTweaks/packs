from beet import Context, subproject
from pathlib import Path

import logging

logger = logging.getLogger(__name__)
logger.setLevel("INFO")


def beet_default(ctx: Context):
    datapacks = ctx.meta.get("datapacks", [])
    zip = ctx.meta.get("zip", False)
    items = Path("datapacks").iterdir()

    filtered = filter(
        lambda item: (item.name in datapacks) if datapacks else True, items
    )

    for file in filtered:
        if file.is_dir():
            try:
                logger.info("Building Project %s", file)

                ctx.require(
                    subproject(
                        {
                            "directory": str(file),
                            "output": "../../dist",
                            "extend": ["beet.yaml"],
                            "require": ["bolt"],
                            "pipeline": [
                                "mecha",
                            ],
                            "data_pack": {"zipped": zip},
                            "resource_pack": {"zipped": zip},
                        }
                    )
                )

            except Exception as err:
                logger.exception(err)
