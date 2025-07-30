"""TDD MCP Server - A Model Context Protocol server for test-driven development."""

try:
    from ._version import __version__
except ImportError:
    # Fallback for development mode when package isn't installed
    from importlib.metadata import PackageNotFoundError, version

    try:
        __version__ = version("tdd-mcp-server")
    except PackageNotFoundError:
        __version__ = "unknown"
