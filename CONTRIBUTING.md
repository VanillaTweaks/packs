# Contributing

Contributions are welcome. Make sure to first open an issue discussing the problem or the new feature before creating a pull request.

## Python

The project must type-check with [`pyright`](https://github.com/microsoft/pyright). If you're using VS Code the [`pylance`](https://marketplace.visualstudio.com/items?itemName=ms-python.vscode-pylance) extension should report diagnostics automatically.

The code follows the [`black`](https://github.com/psf/black) code style. Import statements are sorted with [`isort`](https://pycqa.github.io/isort/).

```bash
poetry run isort lib
poetry run black lib
poetry run black --check lib
```
