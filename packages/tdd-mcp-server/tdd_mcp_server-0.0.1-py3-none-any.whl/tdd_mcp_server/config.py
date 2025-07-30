"""Configuration management for TDD MCP Server."""

from __future__ import annotations

import os
import sys
from dataclasses import dataclass
from typing import Any

if sys.version_info >= (3, 11):
    import tomllib
else:
    import tomli as tomllib


@dataclass
class ToolConfig:
    """Configuration for a single command-line tool."""

    name: str
    description: str
    command: str
    args: list[str]
    expected_runtime_seconds: float
    expected_output_size_bytes: int
    working_directory: str | None = None
    environment_variables: dict[str, str] | None = None
    timeout_seconds: float | None = None
    frozen_args: bool = False


@dataclass
class TDDConfig:
    """Main configuration for the TDD MCP Server."""

    tools: dict[str, ToolConfig]
    cache_directory: str = ".tdd-mcp-cache"
    max_cache_size_mb: int = 100
    max_history_entries: int = 1000


def load_config(config_path: str | None = None) -> TDDConfig:
    """Load configuration from TOML file."""
    if config_path is None:
        # Look for config file in current directory first, then user home
        config_path = "tdd-mcp-config.toml"
        if not os.path.exists(config_path):
            config_path = os.path.expanduser("~/.tdd-mcp-config.toml")
            if not os.path.exists(config_path):
                # Create a default config if none exists
                return TDDConfig(tools={})

    try:
        with open(config_path, "rb") as f:
            config_data: dict[str, Any] = tomllib.load(f)
    except FileNotFoundError:
        return TDDConfig(tools={})
    except Exception as e:
        raise ValueError(f"Failed to parse config file {config_path}: {e}")

    # Parse tools
    tools: dict[str, ToolConfig] = {}
    for tool_name, tool_data in config_data.get("tools", {}).items():
        tools[tool_name] = ToolConfig(
            name=tool_name,
            description=tool_data.get("description", ""),
            command=tool_data.get("command", tool_name),
            args=tool_data.get("args", []),
            expected_runtime_seconds=tool_data.get("expected_runtime_seconds", 1.0),
            expected_output_size_bytes=tool_data.get(
                "expected_output_size_bytes", 1024
            ),
            working_directory=tool_data.get("working_directory"),
            environment_variables=tool_data.get("environment_variables"),
            timeout_seconds=tool_data.get("timeout_seconds"),
            frozen_args=tool_data.get("frozen_args", False),
        )

    # Parse global settings
    cache_directory: str = config_data.get("cache_directory", ".tdd-mcp-cache")
    # Expand user home directory if path starts with ~
    cache_directory = os.path.expanduser(cache_directory)
    max_cache_size_mb: int = config_data.get("max_cache_size_mb", 100)
    max_history_entries: int = config_data.get("max_history_entries", 1000)

    return TDDConfig(
        tools=tools,
        cache_directory=cache_directory,
        max_cache_size_mb=max_cache_size_mb,
        max_history_entries=max_history_entries,
    )


def create_example_config(path: str = "tdd-mcp-config.toml") -> None:
    """Create an example configuration file."""
    example_config: str = """# TDD MCP Server Configuration

# Global settings
cache_directory = ".tdd-mcp-cache"
max_cache_size_mb = 100
max_history_entries = 1000

# Tool definitions
[tools.pytest]
description = "Run Python tests using pytest"
command = "pytest"
args = ["-v", "--tb=short"]
expected_runtime_seconds = 5.0
expected_output_size_bytes = 2048
working_directory = "."
timeout_seconds = 60.0

[tools.npm_test]
description = "Run JavaScript/TypeScript tests using npm"
command = "npm"
args = ["test"]
expected_runtime_seconds = 3.0
expected_output_size_bytes = 1024
working_directory = "."
timeout_seconds = 30.0

[tools.cargo_test]
description = "Run Rust tests using cargo"
command = "cargo"
args = ["test"]
expected_runtime_seconds = 10.0
expected_output_size_bytes = 4096
working_directory = "."
timeout_seconds = 120.0

[tools.go_test]
description = "Run Go tests"
command = "go"
args = ["test", "./..."]
expected_runtime_seconds = 2.0
expected_output_size_bytes = 1024
working_directory = "."
timeout_seconds = 30.0

[tools.mypy]
description = "Run Python type checking with mypy"
command = "mypy"
args = ["."]
expected_runtime_seconds = 8.0
expected_output_size_bytes = 2048
working_directory = "."
timeout_seconds = 60.0

[tools.eslint]
description = "Run JavaScript/TypeScript linting with ESLint"
command = "npx"
args = ["eslint", ".", "--format=compact"]
expected_runtime_seconds = 3.0
expected_output_size_bytes = 1024
working_directory = "."
timeout_seconds = 30.0

[tools.security_scan]
description = "Run security vulnerability scan (frozen args)"
command = "safety"
args = ["check", "--json"]
expected_runtime_seconds = 5.0
expected_output_size_bytes = 2048
working_directory = "."
timeout_seconds = 60.0
frozen_args = true
"""

    with open(path, "w") as f:
        f.write(example_config)
