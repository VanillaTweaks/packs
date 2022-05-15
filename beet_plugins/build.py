import logging
import re
from pathlib import Path

import yaml
from beet import Context, subproject

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

    pack_pattern = ctx.meta.get("packs")
    if not isinstance(pack_pattern, str):
        raise TypeError(
            f"The following value of `packs` is not a string:\n{repr(pack_pattern)}"
        )

    pack_paths = Path(".").glob(pack_pattern)

    # A mapping from each pack's path to a dictionary of the pack's config.
    pack_configs: dict[Path, dict[str, object]] = {}

    for pack_path in pack_paths:
        if not pack_path.is_dir():
            continue

        if VALID_PATH.match(pack_path.as_posix()):
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

    for pack_path in pack_paths:
        try:
            logger.info("Building %s...", pack_path)

            pack_config = pack_configs[pack_path]

            game_version = pack_path.parts[1]

            ctx.require(
                subproject(
                    {
                        "id": pack_path.name,
                        "name": pack_config["title"],
                        "version": pack_config["version"],
                        "directory": str(pack_path),
                        "output": "../../../dist",
                        "data_pack": {
                            "load": [".", {f"data/{pack_path.name}/modules": "."}],
                            "description": [
                                {
                                    "text": f"{pack_config['title']} {pack_config['version']} for MC {game_version}",
                                    "color": "gold",
                                },
                                {"text": "\nvanillatweaks.net", "color": "yellow"},
                            ],
                        },
                        "require": ["bolt"],
                        "pipeline": ["mecha"],
                        "meta": {"pack_config": pack_config},
                    }
                )
            )

        except Exception as error:
            logger.exception(error)
