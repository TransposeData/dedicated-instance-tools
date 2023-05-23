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
```

### Modules
Select the module you're interested in below:

| Module | Description                                          | Documentation        |
| ------ | ---------------------------------------------------- | -------------------- |
| Sync   | Utilities for pulling data from a dedicated instance | [View](sync.md) |
