# Dedicated Instance Tools
![Deployment Tests](https://github.com/TransposeData/transpose-python-sdk/actions/workflows/deployment_tests.yml/badge.svg) ![PyPI version](https://badge.fury.io/py/transpose-dit.svg) ![Installations](https://img.shields.io/pypi/dd/transpose-dit?color=g)

Python utilities for working with Transpose Dedicated Instances.

## Getting Started

First, install the package from PyPI:

```bash
pip install transpose-dit
```

Then, connecting to your dedicated instance is as easy as

```python
from transpose import DedicatedInstance

db = DedicatedInstance(
    host=os.environ.get("HOST"),
    port=os.environ.get("PORT"),
    user=os.environ.get("USERNAME"),
    password=os.environ.get("PASSWORD"),
    database=os.environ.get("DATABASE"),
    sslmode=os.environ.get("SSLMODE"),
    debug=True,
)

...
```

### Documentation
You can view the full documentation for this package [here](docs), or select the module you're interested in below:

| Module | Description                                          | Documentation        |
| ------ | ---------------------------------------------------- | -------------------- |
| Sync   | Utilities for pulling data from a dedicated instance | [View](docs/sync.md) |

### Examples
You can view examples of how to use this package in the [examples](examples) directory.
