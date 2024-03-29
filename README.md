# Vanilla Tweaks Packs

This is the official repo for the source of some of the Vanilla Tweaks packs.

## Usage

### Setup

Requirements:
* [`python`](https://python.org) 3.11+
* [`poetry`](https://python-poetry.org)

After cloning the repo and installing the above requirements, run the following inside the repo to install dependencies.

```bash
poetry install
```

### Building

You can build a data pack or a set of data packs using `python run.py build` from inside the repo.

Examples:
```sh
python run.py build "datapacks/1.18/better_item_frames"
python run.py build "datapacks/1.18/*"
python run.py build "d*/1.18/*frame*"
```

To continually rebuild the project whenever files are changed, use `python run.py watch` in the same way.

### Outputting Packs to Minecraft

You can use `beet link` to link the build output to your Minecraft directory and/or to a particular world.

For example, if you want to output data packs to a world named "Vanilla Tweaks" in the default Minecraft directory, run the following.

```bash
beet link "Vanilla Tweaks"
```

You only ever need to run this once.

Enter `beet link --help` for more information.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md).
