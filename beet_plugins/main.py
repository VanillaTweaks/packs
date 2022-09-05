import logging
import re
from pathlib import Path

import mecha
import yaml
from beet import Context, subproject

from lib.types import Unknown

logger = logging.getLogger(__name__)
logger.setLevel("INFO")

VALID_PATH = re.compile(r"^(?:data|resource)packs/\d+\.\d+/[^/]+$")


def beet_default(ctx: Context):
    """Plugin to build packs."""

    # TODO: Support resource packs.

    pack_pattern = str(ctx.meta.get("pack_pattern"))
    pack_paths = Path(".").glob(pack_pattern)

    # A mapping from each pack's path to a dictionary of the pack's config.
    pack_configs: dict[Path, dict[str, Unknown]] = {}

    for pack_path in pack_paths:
        if not pack_path.is_dir():
            continue

        if not VALID_PATH.match(pack_path.as_posix()):
            raise ValueError(
                "The following path is not directly in `datapacks/<game version>/` or "
                f"`resourcepacks/<game version>/`:\n{pack_path}"
            )

        pack_config_path = pack_path / "config.yaml"

        if not pack_config_path.is_file():
            raise FileNotFoundError(
                f"The following path does not contain a `config.yaml`:\n{pack_path}"
            )

        pack_configs[pack_path] = yaml.safe_load(pack_config_path.read_text())

    for pack_path, pack_config in pack_configs.items():
        try:
            logger.info("Building %s...", pack_path)

            game_version = pack_path.parts[1]

            namespace = pack_path.name

            description = [
                {
                    "text": (
                        f"{pack_config['title']} {pack_config['version']}"
                        f" for MC {game_version}"
                    ),
                    "color": "gold",
                },
                {"text": "\nvanillatweaks.net", "color": "yellow"},
            ]

            ctx.require(
                subproject(
                    {
                        "id": namespace,
                        "name": pack_config["title"],
                        "version": pack_config["version"],
                        "directory": str(pack_path),
                        "output": "../../../dist",
                        "minecraft": game_version,
                        "data_pack": {
                            "load": [
                                {"data/lib/modules": "../../../lib"},
                                # The `/_` is necessary so `bolt` resource locations
                                #  don't conflict with `mcfunction` resource locations.
                                {f"data/{namespace}/modules/_": "."},
                                # Load the pack as a normal pack directory with a `data`
                                #  folder.
                                ".",
                            ],
                            "description": description,
                        },
                        "require": [
                            "beet_plugins.json_helpers.get_custom_json_values",
                            "bolt",
                            "beet_plugins.nbt_literals",
                        ],
                        "pipeline": ["mecha", "beet.contrib.minify_json"],
                        "meta": {
                            "autosave": {"link": True},
                            "bolt": {"entrypoint": f"{namespace}:*"},
                            "pack_config": pack_config,
                        },
                    }
                )
            )

        except mecha.diagnostic.DiagnosticErrorSummary:
            pass

        # TODO: log error but avoid the bubble up
        # except Exception as error:
        #     logger.exception(error)
