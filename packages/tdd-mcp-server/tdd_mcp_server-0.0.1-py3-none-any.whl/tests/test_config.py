"""Tests for the configuration module."""

import os
import tempfile

from tdd_mcp_server.config import (
    TDDConfig,
    ToolConfig,
    create_example_config,
    load_config,
)


def test_tool_config_creation():
    """Test creating a ToolConfig."""
    config = ToolConfig(
        name="test_tool",
        description="A test tool",
        command="echo",
        args=["hello"],
        expected_runtime_seconds=1.0,
        expected_output_size_bytes=100,
    )

    assert config.name == "test_tool"
    assert config.description == "A test tool"
    assert config.command == "echo"
    assert config.args == ["hello"]
    assert config.expected_runtime_seconds == 1.0
    assert config.expected_output_size_bytes == 100


def test_load_empty_config():
    """Test loading configuration when no file exists."""
    with tempfile.TemporaryDirectory() as temp_dir:
        config_path = os.path.join(temp_dir, "nonexistent.toml")
        config = load_config(config_path)

        assert isinstance(config, TDDConfig)
        assert len(config.tools) == 0
        assert config.cache_directory == ".tdd-mcp-cache"


def test_create_and_load_example_config():
    """Test creating and loading an example configuration."""
    with tempfile.TemporaryDirectory() as temp_dir:
        config_path = os.path.join(temp_dir, "test-config.toml")

        # Create example config
        create_example_config(config_path)
        assert os.path.exists(config_path)

        # Load the config
        config = load_config(config_path)

        # Check that it has the expected tools
        assert len(config.tools) > 0
        assert "pytest" in config.tools
        assert "npm_test" in config.tools

        # Check a specific tool
        pytest_config = config.tools["pytest"]
        assert pytest_config.name == "pytest"
        assert pytest_config.command == "pytest"
        assert isinstance(pytest_config.args, list)
        assert pytest_config.expected_runtime_seconds > 0


def test_load_custom_config():
    """Test loading a custom configuration."""
    config_content = """
cache_directory = "custom-cache"
max_cache_size_mb = 200

[tools.custom_tool]
description = "A custom tool"
command = "ls"
args = ["-la"]
expected_runtime_seconds = 0.5
expected_output_size_bytes = 512
working_directory = "/tmp"
timeout_seconds = 10.0

[tools.custom_tool.environment_variables]
TEST_VAR = "test_value"

[tools.frozen_tool]
description = "A tool with frozen args"
command = "echo"
args = ["hello", "world"]
expected_runtime_seconds = 0.1
expected_output_size_bytes = 32
frozen_args = true
"""

    with tempfile.NamedTemporaryFile(mode="w", suffix=".toml", delete=False) as f:
        f.write(config_content)
        config_path = f.name

    try:
        config = load_config(config_path)

        assert config.cache_directory == "custom-cache"
        assert config.max_cache_size_mb == 200
        assert len(config.tools) == 2

        # Test regular tool (frozen_args should default to False)
        tool = config.tools["custom_tool"]
        assert tool.name == "custom_tool"
        assert tool.description == "A custom tool"
        assert tool.command == "ls"
        assert tool.args == ["-la"]
        assert tool.expected_runtime_seconds == 0.5
        assert tool.expected_output_size_bytes == 512
        assert tool.working_directory == "/tmp"
        assert tool.timeout_seconds == 10.0
        assert tool.frozen_args is False  # Should default to False

        # Test frozen tool
        frozen_tool = config.tools["frozen_tool"]
        assert frozen_tool.name == "frozen_tool"
        assert frozen_tool.frozen_args is True

    finally:
        os.unlink(config_path)
