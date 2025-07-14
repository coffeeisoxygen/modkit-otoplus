import json
from datetime import date, datetime
from typing import Any


class NotSerializableTypeError(TypeError):
    def __init__(self, obj: Any):
        super().__init__(f"Type {type(obj)} not serializable")


def json_default(obj: Any):
    """Serialize an object to a JSON-compatible format.

    This function is used as a default handler for the JSON encoder to
    convert non-serializable objects into a format that can be serialized.

    Args:
        obj (Any): The object to serialize.

    Raises:
        TypeError: If the object is not serializable.

    Returns:
        str: The JSON-compatible string representation of the object.
    """
    if isinstance(obj, (datetime, date)):
        return obj.isoformat()
    raise NotSerializableTypeError(obj)


def dumps(obj: Any) -> str:
    """Serialize an object to a JSON-formatted string.

    This function uses a custom JSON encoder to handle non-serializable
    objects such as datetime and date.

    Args:
        obj (Any): The object to serialize.

    Returns:
        str: The JSON-formatted string.
    """
    return json.dumps(obj, default=json_default)
