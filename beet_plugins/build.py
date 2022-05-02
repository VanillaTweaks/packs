import logging
from pathlib import Path

import yaml
from beet import Context, subproject
from bolt import Runtime

from lib.resource_location import ResourceLocation
import re

logger = logging.getLogger(__name__)
logger.setLevel("INFO")

VALID_PATH = re.compile(r"^(?:data|resource)packs/\d+\.\d+/[^/]+$")


def beet_default(ctx: Context):
    """Plugin to build packs.

    Examples:
    ```sh
    beet -s 'meta.packs="datapacks/1.18/invisible_item_frames"'
    beet -s 'meta.packs="datapacks/1.18/*frame*"'
    beet -s 'meta.packs="datapacks/1.18/*"'
    ```
    """

    # TODO: Support resource packs.

    pattern: str | None = ctx.meta.get("packs")
    assert isinstance(pattern, str)
    paths = Path(".").glob(pattern)

    pack_configs: dict[Path, dict[str, str]] = {}

    for path in paths:
        if not path.is_dir():
            continue

        if VALID_PATH.match(path.as_posix()):
            raise ValueError(
                f"The following path is not directly in `datapacks/<game version>/` or `resourcepacks/<game version>/`:\n{path}"
            )

        pack_config_path = path / "pack.yaml"
        if not pack_config_path.is_file():
            raise FileNotFoundError(
                f"The following path does not contain a `pack.yaml`:\n{path}"
            )

        pack_configs[path] = yaml.safe_load(pack_config_path.read_text())

    for path in paths:
        try:
            logger.info(f"Building {path}...")

            pack_config = pack_configs[path]

            game_version = path.parts[1]

            ctx.require(
                subproject(
                    {
                        "id": path.name,
                        "name": pack_config["title"],
                        "version": pack_config["version"],
                        "directory": str(path),
                        "output": "../../../dist",
                        "data_pack": {
                            "load": [".", {f"data/{path.name}/modules": "."}],
                            "description": [
                                {
                                    "text": f"{pack_config['title']} {pack_config['version']} for MC {game_version}",
                                    "color": "gold",
                                },
                                {"text": "\nvanillatweaks.net", "color": "yellow"},
                            ],
                        },
                        "require": ["beet_plugins.build.expose_globals", "bolt"],
                        "pipeline": [
                            "mecha",
                        ],
                    }
                )
            )
        except Exception as error:
            logger.exception(error)


def expose_globals(ctx: Context):
    runtime = ctx.inject(Runtime)
    runtime.globals["pack"] = ResourceLocation(
        ctx.project_id,
        version=ctx.project_version,
        title=ctx.project_name,
    )
