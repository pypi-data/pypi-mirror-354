"""Image models for Apple Container.

Based on the official Apple Container repository structures:
- Sources/ContainerClient/Core/ImageDescription.swift
"""

from datetime import datetime
from typing import Any

from .base import AppleContainerBaseModel


class ImageDescription(AppleContainerBaseModel):
    """Container image description.

    Based on Apple Container's ImageDescription struct.
    """

    reference: str  # Image reference (e.g., "ubuntu:latest")

    @property
    def repository(self) -> str:
        """Get repository name from reference."""
        if ":" in self.reference:
            return self.reference.split(":")[0]
        return self.reference

    @property
    def tag(self) -> str:
        """Get tag from reference."""
        if ":" in self.reference:
            return self.reference.split(":", 1)[1]
        return "latest"

    @property
    def full_name(self) -> str:
        """Get full image name."""
        return self.reference

    def __str__(self) -> str:
        return f"ImageDescription({self.reference})"


# Legacy compatibility - simplified Image model
class Image(AppleContainerBaseModel):
    """Container image (legacy compatibility)."""

    id: str
    repository: str
    tag: str
    digest: str | None = None
    size: int | None = None
    created_at: datetime | None = None
    labels: dict[str, str] | None = None
    architecture: str | None = None
    os: str | None = None

    @property
    def full_name(self) -> str:
        """Get full image name with tag."""
        return f"{self.repository}:{self.tag}"

    @property
    def short_id(self) -> str:
        """Get short image ID (first 12 characters)."""
        return self.id[:12]

    def __str__(self) -> str:
        return f"Image({self.full_name}, id={self.short_id})"


class ImagePullProgress(AppleContainerBaseModel):
    """Image pull progress information (not directly used by Apple Container)."""

    layer_id: str
    status: str
    progress: str | None = None
    current: int | None = None
    total: int | None = None

    @property
    def percentage(self) -> float | None:
        """Calculate percentage complete."""
        if self.current is not None and self.total is not None and self.total > 0:
            return (self.current / self.total) * 100.0
        return None


class ImageBuildContext(AppleContainerBaseModel):
    """Context for building images (not directly used by Apple Container)."""

    dockerfile_path: str
    context_path: str
    tag: str
    build_args: dict[str, str] | None = None
    target: str | None = None
    no_cache: bool = False
    pull: bool = False


class ImageHistory(AppleContainerBaseModel):
    """Image layer history (legacy compatibility)."""

    id: str
    created: datetime
    created_by: str
    size: int
    comment: str | None = None


class ImageInspect(AppleContainerBaseModel):
    """Detailed image information (legacy compatibility)."""

    id: str
    repository: str
    tag: str
    digest: str | None = None
    size: int
    created_at: datetime
    architecture: str
    os: str
    config: dict[str, Any]
    root_fs: dict[str, Any]
    history: list[ImageHistory]
    labels: dict[str, str] | None = None
