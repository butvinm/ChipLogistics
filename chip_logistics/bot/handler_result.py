"""Handlers result structure."""


from typing import Any, Optional, Union

from pydantic import BaseModel, Field


class Ok(BaseModel):
    """Successful handler result."""

    # Extra information about handler execution
    extra: dict[str, Any] = Field(default_factory=dict)


class Err(BaseModel):
    """Failure of handler execution."""

    # Cause error
    error: Optional[str] = None

    # Error message
    message: str

    # Extra information about handler execution
    extra: dict[str, Any] = Field(default_factory=dict)


# Result of handler execution
# Can be used for logging and debugging
HandlerResult = Union[Ok, Err]
