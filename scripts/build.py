import argparse
import subprocess

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
    subprocess.run(
        [
            "beet",
            "-s",
            f"meta.pack_pattern={repr(args.pack_pattern)}",
            beet_command,
        ]
    )
