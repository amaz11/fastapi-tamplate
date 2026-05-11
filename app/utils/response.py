from typing import Any


def success_response(data: Any, message: str = "Success") -> dict[str, Any]:
    return {"message": message, "data": data}
