import logging
import re
from pathlib import Path

import yaml
from beet import Context, subproject

from lib import metadata
from lib.pack_config import PackConfig
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

        pack_config_path = pack_path / "pack.yaml"

        if not pack_config_path.is_file():
            raise FileNotFoundError(
                f"The following path does not contain a `pack.yaml`:\n{pack_path}"
            )

        pack_configs[pack_path] = yaml.safe_load(pack_config_path.read_text())

    for pack_path, pack_config_json in pack_configs.items():
        logger.info("Building %s...", pack_path)

        metadata.game_version = pack_path.parts[1]
        metadata.namespace = pack_path.name
        metadata.pack_config = PackConfig.parse_obj(pack_config_json)

        description = [
            {
                "text": (
                    f"{metadata.pack_config.title} {metadata.pack_config.version}"
                    f" for MC {metadata.game_version}"
                ),
                "color": "gold",
            },
            {"text": "\nvanillatweaks.net", "color": "yellow"},
        ]

        ctx.require(
            subproject(
                {
                    "id": metadata.namespace,
                    "name": metadata.pack_config.title,
                    "version": str(metadata.pack_config.version),
                    "directory": str(pack_path),
                    "output": "../../../dist",
                    "minecraft": metadata.game_version,
                    "data_pack": {
                        "load": [
                            {"data/lib/modules": "../../../lib"},
                            {f"data/pack/modules": "."},
                            # Load the pack as a normal pack directory with a `data`
                            #  folder.
                            ".",
                        ],
                        "description": description,
                    },
                    "require": [
                        "beet_plugins.json_helpers.get_custom_json_values",
                        "bolt",
                        "bolt.contrib.defer",
                        "beet_plugins.nbt_literals",
                        "minecraft_text_components.contrib.beet_minify",
                    ],
                    "pipeline": [
                        "mecha",
                        "beet.contrib.line_endings",
                        "beet.contrib.minify_json",
                        "beet.contrib.strip_final_newlines",
                    ],
                    "meta": {
                        "autosave": {"link": True},
                        # Force LF line endings on all platforms.
                        "line_endings": {"newline": "\n"},
                        "mecha": {"formatting": "minify"},
                        "bolt": {"entrypoint": "pack:*"},
                    },
                }
            )
        )
