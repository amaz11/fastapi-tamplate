from typing import Any


def strip_private_fields(data: dict[str, Any]) -> dict[str, Any]:
    """Remove fields you do not want to return to client."""

    return {key: value for key, value in data.items() if key != "password"}
