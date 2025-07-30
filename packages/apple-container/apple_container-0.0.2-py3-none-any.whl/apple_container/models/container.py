"""Container models for Apple Container.

Based on the official Apple Container repository structures:

Reference implementations:
- ContainerConfiguration: https://github.com/apple/container/blob/main/Sources/ContainerClient/Core/ContainerConfiguration.swift
- ContainerSnapshot: https://github.com/apple/container/blob/main/Sources/ContainerClient/Core/ContainerSnapshot.swift
- ProcessConfiguration: https://github.com/apple/container/blob/main/Sources/ContainerClient/Core/ProcessConfiguration.swift
- ClientContainer: https://github.com/apple/container/blob/main/Sources/ContainerClient/Core/ClientContainer.swift
- Container Exec: https://github.com/apple/container/blob/main/Sources/CLI/Container/ContainerExec.swift
"""

from datetime import datetime
from typing import Any

from .base import AppleContainerBaseModel


class ProcessConfiguration(AppleContainerBaseModel):
    """Configuration for a process within a container.

    Based on Apple Container's ProcessConfiguration.
    """

    command: list[str]
    args: list[str] | None = None
    working_dir: str | None = None
    env: dict[str, str] | None = None
    user: str | None = None


class DNSConfiguration(AppleContainerBaseModel):
    """DNS configuration for containers.

    Matches Apple Container's DNSConfiguration.
    """

    nameservers: list[str] = ["1.1.1.1"]
    domain: str | None = None
    search_domains: list[str] | None = None
    options: list[str] | None = None


class Resources(AppleContainerBaseModel):
    """Resource limits for containers.

    Matches Apple Container's Resources struct.
    """

    cpus: int = 4
    memory_in_bytes: int = 1024 * 1024 * 1024  # 1 GiB
    storage: int | None = None


class ContainerConfiguration(AppleContainerBaseModel):
    """Configuration for creating a container.

    Matches Apple Container's ContainerConfiguration struct.
    """

    id: str
    image: str  # ImageDescription in Swift, simplified as string
    mounts: list[dict[str, Any]] | None = None  # Filesystem mounts
    labels: dict[str, str] | None = None
    sysctls: dict[str, str] | None = None
    networks: list[str] | None = None
    dns: DNSConfiguration | None = None
    rosetta: bool = False
    hostname: str | None = None
    init_process: ProcessConfiguration
    platform: str = "linux/arm64"  # Platform.current equivalent
    resources: Resources | None = None
    runtime_handler: str = "container-runtime-linux"

    def __init__(self, **data: Any) -> None:
        """Initialize container configuration."""
        # Ensure init_process is provided
        if "init_process" not in data and "command" in data:
            data["init_process"] = ProcessConfiguration(command=data["command"])
        super().__init__(**data)


class ContainerState(AppleContainerBaseModel):
    """Container runtime state.

    Simplified representation of container state based on Apple Container patterns.
    """

    id: str
    state: str  # "created", "running", "stopped", etc.
    configuration: ContainerConfiguration | None = None
    pid: int | None = None
    exit_code: int | None = None
    started_at: datetime | None = None
    finished_at: datetime | None = None

    @property
    def is_running(self) -> bool:
        """Check if container is running."""
        return self.state == "running"

    @property
    def is_stopped(self) -> bool:
        """Check if container is stopped."""
        return self.state in ("stopped", "exited")


# Main Container model (legacy compatibility)
class Container(AppleContainerBaseModel):
    """Container instance (simplified for compatibility)."""

    id: str
    image: str
    status: str
    name: str | None = None
    created_at: datetime | None = None
    config: ContainerConfiguration | None = None
    network_settings: dict[str, Any] | None = None

    @property
    def short_id(self) -> str:
        """Get short container ID (first 12 characters)."""
        return self.id[:12]

    @property
    def is_running(self) -> bool:
        """Check if container is running."""
        return self.status.lower() in ("running", "up")

    @property
    def is_stopped(self) -> bool:
        """Check if container is stopped."""
        return self.status.lower() in ("stopped", "exited", "dead")

    def __str__(self) -> str:
        name = self.name or self.short_id
        return f"Container({name}, status={self.status})"


class ContainerLogs(AppleContainerBaseModel):
    """Container logs response."""

    container_id: str
    logs: str
    timestamp: datetime | None = None


class ContainerEvent(AppleContainerBaseModel):
    """Container event."""

    container_id: str
    event_type: str
    timestamp: datetime
    message: str | None = None
    data: dict[str, Any] | None = None


class ContainerStats(AppleContainerBaseModel):
    """Container statistics (not directly supported by Apple Container)."""

    container_id: str
    cpu_usage: float | None = None
    memory_usage: int | None = None
    memory_limit: int | None = None
    network_io: dict[str, int] | None = None
    disk_io: dict[str, int] | None = None
    timestamp: datetime


class ProcessExecConfiguration(AppleContainerBaseModel):
    """Configuration for executing a process in a running container.

    Based on Apple Container's process execution patterns:
    - ProcessConfiguration: https://github.com/apple/container/blob/main/Sources/ContainerClient/Core/ProcessConfiguration.swift
    - Container Exec CLI: https://github.com/apple/container/blob/main/Sources/CLI/Container/ContainerExec.swift#L45-L65
    - createProcess method: https://github.com/apple/container/blob/main/Sources/ContainerClient/Core/ClientContainer.swift#L186
    """

    id: str  # Process ID
    executable: str  # Command to execute
    arguments: list[str] | None = None
    working_directory: str | None = None
    environment: dict[str, str] | None = None
    user: str | None = None
    terminal: bool = False  # TTY mode
    interactive: bool = False  # Interactive mode
    supplemental_groups: list[str] | None = None

    def __init__(self, **data: Any) -> None:
        """Initialize process exec configuration."""
        if "arguments" not in data and "command" in data:
            # Handle legacy 'command' parameter
            command = data.pop("command")
            if isinstance(command, list) and len(command) > 0:
                data["executable"] = command[0]
                data["arguments"] = command[1:] if len(command) > 1 else []
            elif isinstance(command, str):
                data["executable"] = command
        super().__init__(**data)
