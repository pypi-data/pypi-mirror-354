# make-slice

Creates slice objects with clean syntax.

![](https://img.shields.io/github/license/0x00-pl/make_slice.svg)
[![PyPI](https://img.shields.io/pypi/v/make-slice?logo=pypi&label=PyPI%20package)](https://pypi.org/project/make-slice/)
![](https://img.shields.io/github/release/0x00-pl/make_slice)
![cov](https://0x00-pl.github.io/make_slice/badges/coverage.svg)
![](https://img.shields.io/github/issues/0x00-pl/make_slice)
![](https://img.shields.io/github/stars/0x00-pl/make_slice)

## Install

```bash
pip install make-slice
```

## Usage

```python
from make_slice import make_slice

my_list = list(range(5))  # list: [0, 1, 2, 3, 4]
# Create a slice object
rev_slice = make_slice[::-1]  # Equivalent to slice(None, None, -1)
# Use the slice object
print(my_list[rev_slice])  # Output: [4, 3, 2, 1, 0]
```

## Documentation

Online Documentation is available at [0x00-pl.github.io/make_slice](https://0x00-pl.github.io/make_slice/).

Local server Documentation can be started using `mkdocs`:

```bash
mkdocs serve  # Serves the Documentation at localhost:8000 by default.
```

Offline Documentation can be built using `mkdocs`:

```bash
mkdocs build  # Generates static Documentation files in the 'site' directory.
```

## Development

use `poetry` to manage dependencies and virtual environments:

```bash
pip install poetry
poetry install
```

use `pre-commit` to run reformatting and linting:

```bash
pre-commit install
pre-commit autoupdate
pre-commit run --all-files
```

If you got `files were modified by this hook` when running `git commit`,
you can run `git add .` to stage the changes and then commit again.

## License

MIT License - See [LICENSE](LICENSE) for details.
