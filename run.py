import argparse
import json
import subprocess
from contextlib import suppress

parser = argparse.ArgumentParser(description="Build packs.")
parser.add_argument("action", help="'build' or 'watch'", choices=["build", "watch"])
parser.add_argument(
    "pack_pattern", help="a glob pattern for the pack directories to build or watch"
)
args = parser.parse_args()

with suppress(KeyboardInterrupt):
    subprocess.run(
        [
            "beet",
            "-s",
            f"meta.pack_pattern={json.dumps(args.pack_pattern)}",
            args.action,
        ]
    )
