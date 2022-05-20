import argparse
import json
import subprocess
from contextlib import suppress

parser = argparse.ArgumentParser(description="Build packs.")
parser.add_argument(
    "pack_pattern", help="a glob pattern for the pack directories to build or watch"
)
args = parser.parse_args()


def build():
    run("build")


def watch():
    run("watch")


def run(beet_command: str):
    with suppress(KeyboardInterrupt):
        subprocess.run(
            [
                "beet",
                "-s",
                f"meta.pack_pattern={json.dumps(args.pack_pattern)}",
                beet_command,
            ]
        )
