"""Custom exceptions for apple-container-py."""


class AppleContainerError(Exception):
    """Base exception for apple-container operations."""


class AppleContainerNotFoundError(AppleContainerError):
    """Raised when container is not found."""


class AppleContainerAPIError(AppleContainerError):
    """Raised when API communication fails."""


class AppleContainerPlatformError(AppleContainerError):
    """Raised when platform is not supported."""


class AppleContainerTimeoutError(AppleContainerError):
    """Raised when operation times out."""


class AppleContainerXPCError(AppleContainerError):
    """Raised when XPC communication fails."""
