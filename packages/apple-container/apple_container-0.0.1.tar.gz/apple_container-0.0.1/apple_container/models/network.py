"""Network models for Apple Container.

Based on the official Apple Container repository structures:
- Sources/Services/ContainerNetworkService/NetworkConfiguration.swift
- Sources/Services/ContainerNetworkService/NetworkState.swift
- Sources/Services/ContainerNetworkService/NetworkMode.swift
"""

from datetime import datetime
from enum import Enum
from typing import Any

from .base import AppleContainerBaseModel


class NetworkMode(str, Enum):
    """Network mode that applies to client containers.

    Currently Apple Container only supports NAT mode.
    """

    nat = "nat"


class NetworkConfiguration(AppleContainerBaseModel):
    """Configuration parameters for network creation.

    Matches Apple Container's NetworkConfiguration struct.
    """

    id: str
    mode: NetworkMode = NetworkMode.nat
    subnet: str | None = None

    def __init__(self, **data: Any) -> None:
        """Initialize network configuration."""
        if "mode" not in data:
            data["mode"] = NetworkMode.nat
        super().__init__(**data)


class NetworkStatus(AppleContainerBaseModel):
    """Network runtime status information.

    Matches Apple Container's NetworkStatus struct.
    """

    address: str
    gateway: str


class NetworkState(AppleContainerBaseModel):
    """Network state representing configuration and runtime attributes.

    Based on Apple Container's NetworkState enum but simplified for Python.
    """

    id: str
    state: str  # "created" or "running"
    configuration: NetworkConfiguration
    status: NetworkStatus | None = None

    @property
    def is_created(self) -> bool:
        """Check if network is in created state."""
        return self.state == "created"

    @property
    def is_running(self) -> bool:
        """Check if network is in running state."""
        return self.state == "running"


class NetworkSettings(AppleContainerBaseModel):
    """Container network settings (legacy structure for Docker compatibility)."""

    network_id: str
    ip_address: str | None = None
    gateway: str | None = None
    subnet: str | None = None
    mac_address: str | None = None
    ports: dict[str, list[dict[str, str]]] | None = None


class EndpointSettings(AppleContainerBaseModel):
    """Network endpoint settings for a container (legacy structure)."""

    network_id: str
    endpoint_id: str
    gateway: str
    ip_address: str
    ip_prefix_len: int
    ipv6_gateway: str | None = None
    global_ipv6_address: str | None = None
    global_ipv6_prefix_len: int | None = None
    mac_address: str
    aliases: list[str] | None = None


class NetworkInspect(AppleContainerBaseModel):
    """Detailed network information (legacy structure)."""

    id: str
    name: str
    driver: str
    mode: str
    scope: str
    created_at: datetime
    subnet: str | None = None
    gateway: str | None = None
    ip_range: str | None = None
    containers: dict[str, EndpointSettings]
    options: dict[str, str]
    labels: dict[str, str]
    enable_ipv6: bool = False
    internal: bool = False
    attachable: bool = True


class NetworkConnectConfig(AppleContainerBaseModel):
    """Configuration for connecting a container to a network (legacy structure)."""

    container_id: str
    network_id: str
    aliases: list[str] | None = None
    ip_address: str | None = None
