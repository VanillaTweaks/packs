## Contributing

Contributions are welcome. Make sure to first open an issue discussing the problem or the new feature before creating a pull request.

### Minecraft

This project uses [`beet`](https://github.com/mcbeet/beet) for building.

*TODO*

### Python

The project uses [`poetry`](https://python-poetry.org) for dependency management.

```bash
$ poetry install
```

The project must type-check with [`pyright`](https://github.com/microsoft/pyright). If you're using VSCode the [`pylance`](https://marketplace.visualstudio.com/items?itemName=ms-python.vscode-pylance) extension should report diagnostics automatically.

The code follows the [`black`](https://github.com/psf/black) code style. Import statements are sorted with [`isort`](https://pycqa.github.io/isort/).

```bash
$ poetry run isort vanillatweaks
$ poetry run black vanillatweaks
$ poetry run black --check vanillatweaks
```
