"""Base models for apple-container-py.

Reference implementations:
- Apple Container Repository: https://github.com/apple/container
- Swift Models: https://github.com/apple/container/tree/main/Sources/ContainerClient/Core
- Containerization Library: https://github.com/apple/container/tree/main/Sources/Containerization
"""

from typing import Any

from pydantic import BaseModel, ConfigDict


class AppleContainerBaseModel(BaseModel):
    """Base model for all apple-container objects."""

    model_config = ConfigDict(extra="forbid", validate_assignment=True, arbitrary_types_allowed=True)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "AppleContainerBaseModel":
        """Create instance from dictionary."""
        return cls(**data)

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary."""
        return self.model_dump(exclude_none=True)
