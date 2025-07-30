"""XPC route definitions based on the official Apple Container repository.

Reference implementations:
- XPC Routes: https://github.com/apple/container/blob/main/Sources/ContainerClient/XPC%2B.swift
- Route Definitions: https://github.com/apple/container/blob/main/Sources/ContainerClient/XPCRoute.swift
- XPC Keys: https://github.com/apple/container/blob/main/Sources/ContainerClient/XPCKeys.swift
- API Server Routes: https://github.com/apple/container/blob/main/Sources/APIServer/APIServer.swift
"""

from enum import Enum


class XPCRoute(Enum):
    """XPC routes for Apple Container API.

    These routes match the official Apple Container implementation.
    """

    # Health check
    ping = "ping"

    # Container operations
    listContainer = "listContainer"
    createContainer = "createContainer"
    deleteContainer = "deleteContainer"
    containerLogs = "containerLogs"
    containerEvent = "containerEvent"

    # Plugin operations
    pluginLoad = "pluginLoad"
    pluginGet = "pluginGet"
    pluginRestart = "pluginRestart"
    pluginUnload = "pluginUnload"
    pluginList = "pluginList"

    # Network operations
    networkCreate = "networkCreate"
    networkDelete = "networkDelete"
    networkList = "networkList"

    # Kernel operations
    installKernel = "installKernel"
    getDefaultKernel = "getDefaultKernel"


class XPCKeys(Enum):
    """XPC message keys for Apple Container API.

    These keys match the official Apple Container implementation.
    """

    # Special XPC message keys
    route = "route"
    error = "error"

    # Container keys
    containers = "containers"
    id = "id"
    processIdentifier = "processIdentifier"
    containerConfig = "containerConfig"
    containerOptions = "containerOptions"
    port = "port"
    exitCode = "exitCode"
    containerEvent = "containerEvent"
    fd = "fd"
    logs = "logs"
    stopOptions = "stopOptions"

    # Plugin keys
    pluginName = "pluginName"
    plugins = "plugins"
    plugin = "plugin"

    # Health check
    ping = "ping"

    # Process keys
    signal = "signal"
    snapshot = "snapshot"
    stdin = "stdin"
    stdout = "stdout"
    stderr = "stderr"
    status = "status"
    width = "width"
    height = "height"
    processConfig = "processConfig"

    # Progress update keys
    progressUpdateEndpoint = "progressUpdateEndpoint"
    progressUpdateSetDescription = "progressUpdateSetDescription"
    progressUpdateSetSubDescription = "progressUpdateSetSubDescription"
    progressUpdateSetItemsName = "progressUpdateSetItemsName"
    progressUpdateAddTasks = "progressUpdateAddTasks"
    progressUpdateSetTasks = "progressUpdateSetTasks"
    progressUpdateAddTotalTasks = "progressUpdateAddTotalTasks"
    progressUpdateSetTotalTasks = "progressUpdateSetTotalTasks"
    progressUpdateAddItems = "progressUpdateAddItems"
    progressUpdateSetItems = "progressUpdateSetItems"
    progressUpdateAddTotalItems = "progressUpdateAddTotalItems"
    progressUpdateSetTotalItems = "progressUpdateSetTotalItems"
    progressUpdateAddSize = "progressUpdateAddSize"
    progressUpdateSetSize = "progressUpdateSetSize"
    progressUpdateAddTotalSize = "progressUpdateAddTotalSize"
    progressUpdateSetTotalSize = "progressUpdateSetTotalSize"

    # Network keys
    networkId = "networkId"
    networkConfig = "networkConfig"
    networkState = "networkState"
    networkStates = "networkStates"

    # Kernel keys
    kernel = "kernel"
    kernelTarURL = "kernelTarURL"
    kernelFilePath = "kernelFilePath"
    systemPlatform = "systemPlatform"


# XPC Constants from Apple Container
class XPCConstants:
    """XPC constants used by Apple Container."""

    # Service identifier
    SERVICE_NAME = "com.apple.container.apiserver"

    # Message keys
    ROUTE_KEY = "com.apple.container.xpc.route"
    ERROR_KEY = "com.apple.container.xpc.error"
