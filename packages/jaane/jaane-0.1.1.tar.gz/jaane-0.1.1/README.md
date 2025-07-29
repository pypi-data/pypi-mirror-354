
# jaane

This is a Python package named `jaane`.

## Features
- Simple class `jaane` with a `hi()` method.

## Installation
```bash
pip install .
```

## Usage
```python
from jaane.jaane import jaane
print(jaane.hi())
```

## Development
Install dependencies for development:
```bash
pip install -e .[dev]
```

## License
See [LICENCE](LICENCE) for details.

---

## Project Structure
- `src/jaane/` — Package source code
- `test/` — Tests
- `pyproject.toml` — Build configuration
- `LICENCE` — License file

---

## How to set up `pyproject.toml`

Here is a minimal example for a Python package using [PEP 621](https://www.python.org/dev/peps/pep-0621/):

```toml
[build-system]
requires = ["setuptools>=61.0"]
build-backend = "setuptools.build_meta"

[project]
name = "jaane"
version = "0.1.0"
description = "A simple Python package."
authors = [
    { name = "Your Name", email = "your@email.com" }
]
readme = "README.md"
license = { file = "LICENCE" }
requires-python = ">=3.7"
classifiers = [
    "Programming Language :: Python :: 3",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",
]
dependencies = []

[project.optional-dependencies]
dev = ["pytest"]

[tool.setuptools.packages.find]
where = ["src"]
```

Replace the author and email with your details. Adjust dependencies as needed.
