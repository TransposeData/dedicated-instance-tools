# Sync
The sync module is a utility class for pulling data from a Transpose dedicated instance.

The `DedicatedInstance::sync` class is the main entrypoint for this module. All the heavy-lifting is handled for you, including state management, pagination across table types, and more.

## Getting Started

### Running A Sync Job
To begin a sync, simply call the `DedicatedInstance::sync::run` method, passing in the table you want to sync, and the callback function you want to use to handle the rows.

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

def handle_row(rows: list[dict]) -> bool:
    for row in rows:
        print(row)

    # Return True to continue, False to stop
    return True

db.sync.run(handle_row, "ethereum.native_token_owners", 1_000)
```

This method will automatically handle pagination for you, and will continue to pull rows until the callback function returns `False`.

#### Parameters
| Parameter    | Type                           | Description                                                                                     |
| ------------ | ------------------------------ | ----------------------------------------------------------------------------------------------- |
| `callback`   | `Callable[[list[dict]], bool]` | The callable to pass rows to. This callable should accept a list of rows as it's only argument. |
| `table`      | `str`                          | The table to sync.                                                                              |
| `batch_size` | `int`                          | The number of rows to pull per batch.                                                           |

### Managing State

The sync module automatically handles state management for you, with a few caveats.

- You can load the sync state from a file by using the `DedicatedInstance::sync::load_metadata` method.
  - The only optional parameter is `path`, which defaults to `./metadata.json`.
- You can save the sync state to a file by using the `DedicatedInstance::sync::save_metadata` method.
  - The only optional parameter is `path`, which defaults to `./metadata.json`.
- If you want to manage the state yourself, you can update `DedicatedInstance::sync::metadata` directly.

For example, the following code will run a single batch, and then save the metadata to a file.

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

def handle_row(rows: list[dict]) -> bool:
    for row in rows:
        print(row)

    return False

db.sync.run(handle_row, "ethereum.native_token_owners", 1_000)
db.sync.save_metadata()
```

Likewise, we can load the metadata from a file, and then run the sync job.

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

def handle_row(rows: list[dict]) -> bool:
    for row in rows:
        print(row)

    return False

db.sync.load_metadata()
db.sync.run(handle_row, "ethereum.native_token_owners", 1_000)
```

## Examples
You can find all sync examples [here](../examples/).
