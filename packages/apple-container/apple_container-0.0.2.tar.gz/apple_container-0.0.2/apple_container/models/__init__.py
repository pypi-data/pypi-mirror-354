"""Models for Apple Container.

Based on the official Apple Container repository structures to ensure compatibility
with the actual Apple Container implementation.

Reference implementations:
- Apple Container Repository: https://github.com/apple/container
- Core Models: https://github.com/apple/container/tree/main/Sources/ContainerClient/Core
- Network Service: https://github.com/apple/container/tree/main/Sources/Services/ContainerNetworkService
- Configuration Models: https://github.com/apple/container/tree/main/Sources/Containerization

Key model mappings:
- Container: ClientContainer.swift -> container.py
- Network: NetworkConfiguration.swift -> network.py
- Image: ImageDescription.swift -> image.py
- Process: ProcessConfiguration.swift -> container.py
"""

from .base import AppleContainerBaseModel
from .container import (
    Container,
    ContainerConfiguration,
    ContainerEvent,
    ContainerLogs,
    ContainerState,
    ContainerStats,
    DNSConfiguration,
    ProcessConfiguration,
    ProcessExecConfiguration,
    Resources,
)
from .image import Image, ImageBuildContext, ImageDescription, ImageHistory, ImageInspect, ImagePullProgress
from .network import (
    EndpointSettings,
    NetworkConfiguration,
    NetworkConnectConfig,
    NetworkInspect,
    NetworkMode,
    NetworkSettings,
    NetworkState,
    NetworkStatus,
)

__all__ = [
    # Base
    "AppleContainerBaseModel",
    # Container models (Apple Container official)
    "ContainerConfiguration",
    "ContainerState",
    "ProcessConfiguration",
    "ProcessExecConfiguration",
    "DNSConfiguration",
    "Resources",
    # Container models (legacy compatibility)
    "Container",
    "ContainerEvent",
    "ContainerLogs",
    "ContainerStats",
    # Image models (Apple Container official)
    "ImageDescription",
    # Image models (legacy compatibility)
    "Image",
    "ImageBuildContext",
    "ImageHistory",
    "ImageInspect",
    "ImagePullProgress",
    # Network models (Apple Container official)
    "NetworkConfiguration",
    "NetworkState",
    "NetworkStatus",
    "NetworkMode",
    # Network models (legacy compatibility)
    "EndpointSettings",
    "NetworkConnectConfig",
    "NetworkInspect",
    "NetworkSettings",
]
