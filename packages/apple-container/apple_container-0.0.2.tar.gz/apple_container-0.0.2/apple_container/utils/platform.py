"""Platform detection utilities."""

import platform
import subprocess


def is_macos() -> bool:
    """Check if running on macOS."""
    return platform.system() == "Darwin"


def is_apple_silicon() -> bool:
    """Check if running on Apple Silicon."""
    if not is_macos():
        return False

    try:
        result = subprocess.run(
            ["sysctl", "-n", "machdep.cpu.brand_string"], capture_output=True, text=True, check=True
        )
        return "Apple" in result.stdout
    except (subprocess.CalledProcessError, FileNotFoundError):
        # Fallback to architecture check
        return platform.machine() == "arm64"


def get_macos_version() -> str | None:
    """Get macOS version."""
    if not is_macos():
        return None

    try:
        result = subprocess.run(["sw_vers", "-productVersion"], capture_output=True, text=True, check=True)
        return result.stdout.strip()
    except (subprocess.CalledProcessError, FileNotFoundError):
        return None


def is_container_available() -> bool:
    """Check if Apple Container CLI is available."""
    try:
        result = subprocess.run(["container", "--version"], capture_output=True, text=True, check=True)
        return result.returncode == 0
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False


def check_platform_compatibility() -> None:
    """Check if platform is compatible with Apple Container."""
    from ..errors import AppleContainerPlatformError

    if not is_macos():
        raise AppleContainerPlatformError("Apple Container is only supported on macOS")

    if not is_apple_silicon():
        raise AppleContainerPlatformError("Apple Container requires Apple Silicon (M1/M2/M3)")

    macos_version = get_macos_version()
    if macos_version and macos_version < "15.0":
        raise AppleContainerPlatformError(f"Apple Container requires macOS 15.0+, got {macos_version}")
