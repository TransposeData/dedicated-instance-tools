import json


def write_json_to_file(object: dict, path: str) -> bool:
    """
    Writes the given object to the given path as JSON.

    :param object: The object to write.
    :param path: The path to write the object to.
    :return: True if the object was written successfully, False otherwise.
    """
    with open(path, "w") as f:
        json.dump(object, f)


def load_json_from_file(path: str) -> dict:
    """
    Loads the given path as JSON.

    :param path: The path to load.
    :return: The loaded JSON object.
    """
    with open(path, "r") as f:
        return json.load(f)
