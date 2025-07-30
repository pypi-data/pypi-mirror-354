[![CI](https://github.com/Y-Square-T3/easyask/actions/workflows/ci.yml/badge.svg)](https://github.com/Y-Square-T3/easyask/actions/workflows/ci.yml)
[![Publish Docker Hub](https://github.com/Y-Square-T3/easyask/actions/workflows/publish-image.yml/badge.svg)](https://hub.docker.com/repository/docker/sheltonsuen/easyask/general)
[![Publish PyPI](https://github.com/Y-Square-T3/easyask/actions/workflows/publish-pypi.yml/badge.svg)](https://pypi.org/project/easyask/)

# easy-ask

easy-ask is a minimal demonstration package intended to show how chart options can be generated programmatically. The
library exposes a function called `generate_option` which accepts a chart type and data description and returns a
configuration dictionary.

## Quick start

```python
from easyask import generate_option

# Build an option for a bar chart
option = generate_option(
    chart_type="bar",
    data=[{"value": 10}, {"value": 20}, {"value": 30}],
    title="Demo Bar Chart",
)
print(option)
```

## Python version

This project requires **Python 3.12** or newer, as specified in `pyproject.toml`.

## Running the demo

To see the package in action, run the demonstration module:

```bash
python -m easyask
```

Example scripts are also available in the `examples/` directory.

## How to test

```bash
PYTHONPATH=. pytest
```
