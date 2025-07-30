"""Apple Container Python SDK.

A Python SDK for interacting with Apple Container via XPC communication.
Provides a Docker-like API for container management on macOS.

This implementation is based on the official Apple Container Swift codebase:
https://github.com/apple/container

Reference Mappings:
================

XPC Communication:
- XPCClient: https://github.com/apple/container/blob/main/Sources/ContainerClient/XPCClient.swift
- XPCMessage: https://github.com/apple/container/blob/main/Sources/ContainerClient/XPCMessage.swift
- Routes: https://github.com/apple/container/blob/main/Sources/ContainerClient/XPC%2B.swift

Container Operations:
- ClientContainer: https://github.com/apple/container/blob/main/Sources/ContainerClient/Core/ClientContainer.swift
- Container Config: https://github.com/apple/container/blob/main/Sources/ContainerClient/Core/ContainerConfiguration.swift
- Container Exec: https://github.com/apple/container/blob/main/Sources/CLI/Container/ContainerExec.swift

Network Operations:
- NetworkConfiguration: https://github.com/apple/container/blob/main/Sources/Services/ContainerNetworkService/NetworkConfiguration.swift
- NetworkState: https://github.com/apple/container/blob/main/Sources/Services/ContainerNetworkService/NetworkState.swift

API Server:
- Server Implementation: https://github.com/apple/container/blob/main/Sources/APIServer/APIServer.swift

Example:
    import asyncio
    from apple_container import AppleContainerClient, ContainerConfiguration

    async def main():
        client = AppleContainerClient()

        # Check if daemon is running
        if await client.ping():
            print("Apple Container daemon is running")

            # List containers
            containers = await client.list_containers()
            print(f"Found {len(containers)} containers")

            # Create and run a container
            config = ContainerConfiguration(
                id="",  # Auto-generated
                image="alpine:latest"
            )
            container = await client.create_container(config)

            # Execute command in container
            exit_code, output = await client.exec_run(container.id, ["echo", "Hello World"])
            print(f"Command output: {output}")
        else:
            print("Apple Container daemon is not running")

    asyncio.run(main())

"""

from .client import AppleContainerClient, exec_container, exec_run, list_containers, ping, run_container
from .errors import (
    AppleContainerError,
    AppleContainerNotFoundError,
    AppleContainerPlatformError,
    AppleContainerXPCError,
)
from .models import (
    Container,
    ContainerConfiguration,
    ContainerLogs,
    ContainerStats,
    Image,
    NetworkConfiguration,
    NetworkState,
)

# Version information
__version__ = "0.1.0"
__author__ = "Apple Container Python"

# Main SDK exports
__all__ = [
    # Client
    "AppleContainerClient",
    # Convenience functions
    "ping",
    "list_containers",
    "run_container",
    "exec_container",
    "exec_run",
    # Models
    "Container",
    "ContainerConfiguration",
    "ContainerLogs",
    "ContainerStats",
    "Image",
    "NetworkConfiguration",
    "NetworkState",
    # Errors
    "AppleContainerError",
    "AppleContainerNotFoundError",
    "AppleContainerPlatformError",
    "AppleContainerXPCError",
]
