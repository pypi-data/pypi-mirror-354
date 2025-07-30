"""Apple Container Python SDK.

A Python SDK for interacting with Apple Container via XPC communication.
Provides a Docker-like API for container management on macOS.

Example:
    import asyncio
    from apple_container import AppleContainerClient, ContainerConfig

    async def main():
        client = AppleContainerClient()

        # Check if daemon is running
        if await client.ping():
            print("Apple Container daemon is running")

            # List containers
            containers = await client.list_containers()
            print(f"Found {len(containers)} containers")

            # Create and run a container
            config = ContainerConfig(
                id="",  # Auto-generated
                image="alpine:latest",
                command=["echo", "Hello World"]
            )
            container = await client.create_container(config)
            await client.start_container(container.id)
        else:
            print("Apple Container daemon is not running")

    asyncio.run(main())

"""

from .client import AppleContainerClient, list_containers, ping, run_container
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
