"""Utilities ofr working with pydantic models."""


import json
from typing import Any

from pydantic import BaseModel


def model_dump(model: BaseModel) -> dict[str, Any]:
    """Dump model to suitable format for deta requests.

    Args:
        model: Pydantic model object.

    Returns:
        JSON-serializable dict for deta requests.
    """
    return json.loads(model.model_dump_json())  # type: ignore
