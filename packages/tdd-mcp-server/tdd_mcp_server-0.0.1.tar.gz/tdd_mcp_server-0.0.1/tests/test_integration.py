"""Integration tests for the TDD MCP Server."""

import os
import tempfile

import pytest

from tdd_mcp_server.config import ToolConfig
from tdd_mcp_server.tool_runner import ToolRunner


@pytest.mark.asyncio
async def test_tool_execution_basic():
    """Test basic tool execution with echo command."""
    with tempfile.TemporaryDirectory() as temp_dir:
        # Create a simple tool config that just echoes some text
        tool_config = ToolConfig(
            name="echo_test",
            description="Echo test message",
            command="echo",
            args=["hello", "world"],
            expected_runtime_seconds=0.1,
            expected_output_size_bytes=50,
            timeout_seconds=5.0,
        )

        # Create tool runner with temporary cache
        cache_dir = os.path.join(temp_dir, "cache")
        tool_runner = ToolRunner(cache_dir)

        # Run the tool in quiet mode
        quiet_result, full_execution = await tool_runner.run_tool(
            tool_config, quiet=True
        )

        # Check quiet result
        assert quiet_result.exit_code == 0
        assert quiet_result.duration_seconds > 0
        assert len(quiet_result.id) > 0
        assert full_execution is None  # Should be None in quiet mode

        # Get the full execution from cache
        execution = tool_runner.get_execution(quiet_result.id)
        assert execution is not None
        assert execution.tool_name == "echo_test"
        assert execution.command == "echo"
        assert execution.args == ["hello", "world"]
        assert execution.exit_code == 0
        assert "hello world" in execution.stdout
        assert execution.stderr == ""


@pytest.mark.asyncio
async def test_tool_execution_with_additional_args():
    """Test tool execution with additional arguments."""
    with tempfile.TemporaryDirectory() as temp_dir:
        tool_config = ToolConfig(
            name="echo_test",
            description="Echo test message",
            command="echo",
            args=["base"],
            expected_runtime_seconds=0.1,
            expected_output_size_bytes=50,
            timeout_seconds=5.0,
        )

        cache_dir = os.path.join(temp_dir, "cache")
        tool_runner = ToolRunner(cache_dir)

        # Run with additional args
        additional_args = ["extra", "args"]
        quiet_result, _ = await tool_runner.run_tool(
            tool_config, additional_args=additional_args, quiet=True
        )

        # Check that the command included both base and additional args
        execution = tool_runner.get_execution(quiet_result.id)
        assert execution.args == ["base", "extra", "args"]
        assert "base extra args" in execution.stdout


@pytest.mark.asyncio
async def test_tool_execution_failure():
    """Test tool execution when command fails."""
    with tempfile.TemporaryDirectory() as temp_dir:
        # Use a command that will fail
        tool_config = ToolConfig(
            name="false_test",
            description="Command that fails",
            command="false",  # Always exits with code 1
            args=[],
            expected_runtime_seconds=0.1,
            expected_output_size_bytes=50,
            timeout_seconds=5.0,
        )

        cache_dir = os.path.join(temp_dir, "cache")
        tool_runner = ToolRunner(cache_dir)

        quiet_result, _ = await tool_runner.run_tool(tool_config, quiet=True)

        # Should have non-zero exit code
        assert quiet_result.exit_code == 1

        execution = tool_runner.get_execution(quiet_result.id)
        assert execution.exit_code == 1


@pytest.mark.asyncio
async def test_runtime_history_tracking():
    """Test that runtime history is tracked correctly."""
    with tempfile.TemporaryDirectory() as temp_dir:
        tool_config = ToolConfig(
            name="echo_test",
            description="Echo test message",
            command="echo",
            args=["test"],
            expected_runtime_seconds=1.0,
            expected_output_size_bytes=50,
            timeout_seconds=5.0,
        )

        cache_dir = os.path.join(temp_dir, "cache")
        tool_runner = ToolRunner(cache_dir)

        # Initially should use config estimate
        estimate_before = tool_runner.get_runtime_estimate("echo_test", tool_config)
        assert estimate_before == 1.0

        # Run the tool multiple times
        for _ in range(3):
            await tool_runner.run_tool(tool_config, quiet=True)

        # Now should use historical average
        estimate_after = tool_runner.get_runtime_estimate("echo_test", tool_config)
        assert estimate_after != 1.0  # Should be different from config
        assert estimate_after > 0  # Should be positive

        # Check that history was recorded
        assert "echo_test" in tool_runner.runtime_history
        assert len(tool_runner.runtime_history["echo_test"]) == 3


@pytest.mark.asyncio
async def test_last_execution_tracking():
    """Test that last execution is tracked correctly."""
    with tempfile.TemporaryDirectory() as temp_dir:
        tool_config = ToolConfig(
            name="echo_test",
            description="Echo test message",
            command="echo",
            args=["test"],
            expected_runtime_seconds=0.1,
            expected_output_size_bytes=50,
            timeout_seconds=5.0,
        )

        cache_dir = os.path.join(temp_dir, "cache")
        tool_runner = ToolRunner(cache_dir)

        # Initially no last execution
        assert tool_runner.get_last_execution() is None

        # Run a tool
        quiet_result, _ = await tool_runner.run_tool(tool_config, quiet=True)

        # Should now have a last execution
        last_execution = tool_runner.get_last_execution()
        assert last_execution is not None
        assert last_execution.id == quiet_result.id

        # Run another tool
        quiet_result2, _ = await tool_runner.run_tool(tool_config, quiet=True)

        # Last execution should be updated
        last_execution2 = tool_runner.get_last_execution()
        assert last_execution2.id == quiet_result2.id
        assert last_execution2.id != quiet_result.id


@pytest.mark.asyncio
async def test_cache_persistence():
    """Test that execution cache persists between ToolRunner instances."""
    with tempfile.TemporaryDirectory() as temp_dir:
        # Create first runner and execute a tool
        runner1 = ToolRunner(temp_dir)
        tool_config = ToolConfig(
            name="test_tool",
            description="Test",
            command="echo",
            args=["first"],
            expected_runtime_seconds=1.0,
            expected_output_size_bytes=100,
        )

        quiet_result1, full_result1 = await runner1.run_tool(tool_config, quiet=False)

        # Create second runner and verify it loads the cache
        runner2 = ToolRunner(temp_dir)
        cached_execution = runner2.get_execution(quiet_result1.id)

        assert cached_execution is not None
        assert cached_execution.id == quiet_result1.id
        assert cached_execution.command == "echo"
        assert cached_execution.args == ["first"]


@pytest.mark.asyncio
async def test_server_frozen_args_validation():
    """Test that the server layer properly validates frozen_args and raises errors."""
    import tempfile

    from tdd_mcp_server.config import TDDConfig
    from tdd_mcp_server.server import TDDMCPServer

    with tempfile.TemporaryDirectory() as temp_dir:
        # Create a config with a frozen tool
        config = TDDConfig(
            tools={
                "frozen_tool": ToolConfig(
                    name="frozen_tool",
                    description="Tool with frozen args",
                    command="echo",
                    args=["frozen", "args"],
                    expected_runtime_seconds=1.0,
                    expected_output_size_bytes=100,
                    frozen_args=True,
                )
            },
            cache_directory=temp_dir,
            max_cache_size_mb=100,
            max_history_entries=1000,
        )

        # Create server with the config
        server = TDDMCPServer()
        server.config = config
        server.tool_runner = ToolRunner(temp_dir)

        # Test that calling frozen tool with additional args raises ValueError
        with pytest.raises(
            ValueError, match="Additional arguments are not allowed for frozen tools"
        ):
            await server._handle_configured_tool_call(
                "frozen_tool", {"args": ["additional", "args"], "quiet": True}
            )

        # Test that calling frozen tool without additional args works
        result = await server._handle_configured_tool_call(
            "frozen_tool", {"quiet": True}
        )

        # Should return a result without error
        assert len(result) == 1
        assert result[0].type == "text"
