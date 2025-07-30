#!/usr/bin/env python3
"""Basic usage example for Apple Container Python SDK.

This example demonstrates how to use the Apple Container Python SDK
to interact with containers, images, and networks via XPC communication.
"""

import asyncio
import sys
from pathlib import Path

# Add the parent directory to the path so we can import apple_container
sys.path.insert(0, str(Path(__file__).parent.parent))

from apple_container import AppleContainerClient
from apple_container.errors import AppleContainerError


async def main() -> None:
    """Demonstrate basic Apple Container SDK usage."""
    # Create a client instance
    client = AppleContainerClient()

    print("Apple Container Python SDK Example")
    print("==================================")

    # Check if Apple Container daemon is running
    print("\n1. Checking daemon status...")
    if await client.ping():
        print("✓ Apple Container daemon is running")
    else:
        print("✗ Apple Container daemon is not running")
        print("  Please start the Apple Container daemon and try again")
        return

    # Get version information
    try:
        version_info = await client.version()
        print(f"✓ Apple Container version: {version_info}")
    except Exception as e:
        print(f"  Could not get version info: {e}")

    # List existing containers
    print("\n2. Listing containers...")
    try:
        containers = await client.list_containers(all=True)
        print(f"✓ Found {len(containers)} containers")
        for container in containers:
            print(f"  - {container.id} ({container.image}) - {container.status}")
    except Exception as e:
        print(f"✗ Error listing containers: {e}")

    # List available images
    print("\n3. Listing images...")
    try:
        images = await client.list_images()
        print(f"✓ Found {len(images)} images")
        for image in images:
            print(f"  - {image.id} ({image.repository}:{image.tag})")
    except Exception as e:
        print(f"✗ Error listing images: {e}")

    # List networks
    print("\n4. Listing networks...")
    try:
        networks = await client.list_networks()
        print(f"✓ Found {len(networks)} networks")
        for network in networks:
            print(f"  - {network.id} ({network.name})")
    except Exception as e:
        print(f"✗ Error listing networks: {e}")

    # Example: Create and run a container (commented out to avoid side effects)
    print("\n5. Example container operations...")
    print("   (Container creation/modification commented out for safety)")

    # Uncomment the following to actually create and run a container:
    """
    try:
        # Create container configuration
        config = ContainerConfig(
            id="",  # Auto-generated
            image="alpine:latest",
            command=["echo", "Hello from Apple Container!"],
            name="apple-container-test"
        )

        # Create the container
        container = await client.create_container(config)
        print(f"✓ Created container: {container.id}")

        # Start the container
        await client.start_container(container.id)
        print(f"✓ Started container: {container.id}")

        # Get container logs
        logs = await client.get_container_logs(container.id)
        print(f"✓ Container logs: {logs.stdout}")

        # Stop and remove the container
        await client.stop_container(container.id)
        await client.remove_container(container.id)
        print(f"✓ Cleaned up container: {container.id}")

    except Exception as e:
        print(f"✗ Error with container operations: {e}")
    """

    print("\nSDK demonstration complete!")


async def quick_example() -> None:
    """Quick example using convenience functions."""
    print("\n" + "=" * 40)
    print("🚀 Quick Example using convenience functions")
    print("=" * 40)

    try:
        # Use convenience functions
        from apple_container import list_containers, ping, run_container

        # Quick ping
        if await ping():
            print("✅ Daemon is running")
        else:
            print("❌ Daemon not running")
            return

        # Quick container list
        containers = await list_containers()
        print(f"📦 Found {len(containers)} containers")

        # Quick run example (if we have an image)
        try:
            container = await run_container("hello-world:latest", name="quick-test", command=["echo", "Quick test!"])
            print(f"🏃 Ran container: {container.short_id}")

            # Clean up
            client = AppleContainerClient()
            await client.stop_container(container.id)
            await client.remove_container(container.id)
            print(f"🧹 Cleaned up container: {container.short_id}")

        except AppleContainerError as e:
            print(f"⚠️  Could not run quick container: {e}")

    except AppleContainerError as e:
        print(f"❌ Quick example error: {e}")


if __name__ == "__main__":
    print("Starting Apple Container Python examples...")

    try:
        # Run main example
        result = asyncio.run(main())

        # Run quick example
        asyncio.run(quick_example())

        sys.exit(result)

    except KeyboardInterrupt:
        print("\n⏹️  Interrupted by user")
        sys.exit(130)
    except Exception as e:
        print(f"💥 Unexpected error: {e}")
        import traceback

        traceback.print_exc()
        sys.exit(1)
