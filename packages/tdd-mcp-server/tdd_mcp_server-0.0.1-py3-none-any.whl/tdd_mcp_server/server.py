"""Main MCP server implementation for TDD workflows."""

from __future__ import annotations

import asyncio
import json
import logging
import os
import signal
import sys
from typing import Any, Callable, NoReturn, TypeVar

from mcp.server import InitializationOptions, NotificationOptions, Server
from mcp.server.stdio import stdio_server
from mcp.types import (
    TextContent,
    Tool,
)

from tdd_mcp_server.config import load_config
from tdd_mcp_server.tool_runner import ToolRunner

logging.basicConfig(level=logging.INFO)
logger: logging.Logger = logging.getLogger(__name__)


# Tool registry for utility tools
tool_schemas: dict[str, Tool] = {}  # name -> Tool schema
tool_implementations: dict[str, Callable[..., Any]] = {}  # name -> async function


_T = TypeVar("_T", bound=Callable[..., Any])


def tool(
    name: str, description: str, input_schema: dict[str, Any]
) -> Callable[[_T], _T]:
    """Decorator to register a tool handler with its schema."""

    def decorator(func: _T) -> _T:
        # Register the tool
        tool_schemas[name] = Tool(
            name=name, description=description, inputSchema=input_schema
        )
        tool_implementations[name] = func
        return func

    return decorator


class TDDMCPServer:
    """TDD MCP Server implementation."""

    def __init__(self, config_path: str | None = None) -> None:
        self.config = load_config(config_path)
        self.tool_runner = ToolRunner(self.config.cache_directory)
        self.server: Server = Server("tdd-mcp-server")

        # Register handlers
        self._register_handlers()

    def _register_handlers(self) -> None:
        """Register MCP server handlers."""

        @self.server.list_tools()
        async def handle_list_tools() -> list[Tool]:
            """List all available tools."""
            tools: list[Tool] = []

            # Add configured tools
            for tool_name, tool_config in self.config.tools.items():
                # Build input schema based on frozen_args setting
                properties: dict[str, Any] = {
                    "quiet": {
                        "type": "boolean",
                        "description": "If true, return only execution ID, exit code, and duration",
                        "default": True,
                    },
                }

                # Only add args parameter if not frozen
                if not tool_config.frozen_args:
                    properties["args"] = {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": f"Additional arguments to pass to {tool_config.command}",
                        "default": [],
                    }

                tools.append(
                    Tool(
                        name=tool_name,
                        description=tool_config.description,
                        inputSchema={
                            "type": "object",
                            "properties": properties,
                        },
                    )
                )

            # Add registered utility tools
            tools.extend(tool_schemas.values())

            return tools

        @self.server.call_tool()
        async def handle_call_tool(
            name: str, arguments: dict[str, Any]
        ) -> list[TextContent]:
            """Handle tool calls."""
            try:
                if name in self.config.tools:
                    return await self._handle_configured_tool_call(name, arguments)
                elif name in tool_implementations:
                    # Call the registered tool implementation
                    return await tool_implementations[name](self, arguments)
                else:
                    raise ValueError(f"Unknown tool: {name}")

            except Exception as e:
                logger.error(f"Error handling tool call {name}: {e}")
                raise RuntimeError(f"Tool execution failed: {str(e)}")

    async def _handle_configured_tool_call(
        self, name: str, arguments: dict[str, Any]
    ) -> list[TextContent]:
        """Handle a call to a configured tool."""
        tool_config = self.config.tools[name]

        # Only allow additional args if not frozen
        if (additional_args := arguments.get("args", [])) and tool_config.frozen_args:
            raise ValueError("Additional arguments are not allowed for frozen tools")

        quiet: bool = arguments.get("quiet", True)

        # Run the tool
        quiet_result, full_execution = await self.tool_runner.run_tool(
            tool_config, additional_args, quiet
        )

        if quiet:
            # Return minimal information
            content: list[TextContent] = [
                TextContent(
                    type="text",
                    text=json.dumps(
                        {
                            "id": quiet_result.id,
                            "exit_code": quiet_result.exit_code,
                            "duration_seconds": round(quiet_result.duration_seconds, 3),
                            "tool_name": name,
                            "status": (
                                "success" if quiet_result.exit_code == 0 else "failure"
                            ),
                        },
                        indent=2,
                    ),
                )
            ]
        else:
            # Return full information
            if full_execution is None:
                raise RuntimeError("Expected full execution but got None")

            content = [
                TextContent(
                    type="text",
                    text=json.dumps(
                        {
                            "id": full_execution.id,
                            "tool_name": full_execution.tool_name,
                            "command": full_execution.command,
                            "args": full_execution.args,
                            "exit_code": full_execution.exit_code,
                            "duration_seconds": round(
                                full_execution.duration_seconds, 3
                            ),
                            "stdout": full_execution.stdout,
                            "stderr": full_execution.stderr,
                            "working_directory": full_execution.working_directory,
                            "timestamp": full_execution.timestamp,
                        },
                        indent=2,
                    ),
                )
            ]

        return content

    @tool(
        name="get_output_for_tool_call_id",
        description="Retrieve the full output (stdout/stderr) for a specific tool execution ID",
        input_schema={
            "type": "object",
            "properties": {
                "id": {
                    "type": "string",
                    "description": "The execution ID returned from a tool call",
                }
            },
            "required": ["id"],
        },
    )
    async def _handle_get_output_for_id(
        self, arguments: dict[str, Any]
    ) -> list[TextContent]:
        """Handle getting output for a specific execution ID."""
        execution_id: str | None = arguments.get("id")
        if not execution_id:
            raise ValueError("Missing required parameter: id")

        execution = self.tool_runner.get_execution(execution_id)
        if not execution:
            raise ValueError(f"No execution found for ID: {execution_id}")

        content: list[TextContent] = [
            TextContent(
                type="text",
                text=json.dumps(
                    {
                        "id": execution.id,
                        "tool_name": execution.tool_name,
                        "command": execution.command,
                        "args": execution.args,
                        "exit_code": execution.exit_code,
                        "duration_seconds": round(execution.duration_seconds, 3),
                        "stdout": execution.stdout,
                        "stderr": execution.stderr,
                        "working_directory": execution.working_directory,
                        "timestamp": execution.timestamp,
                    },
                    indent=2,
                ),
            )
        ]

        return content

    @tool(
        name="get_last_tool_call_output",
        description="Retrieve the full output for the most recent tool execution",
        input_schema={
            "type": "object",
            "properties": {
                "random_string": {
                    "type": "string",
                    "description": "Dummy parameter for no-parameter tools",
                }
            },
            "required": ["random_string"],
        },
    )
    async def _handle_get_last_output(
        self, arguments: dict[str, Any]
    ) -> list[TextContent]:
        """Handle getting output for the last execution."""
        execution = self.tool_runner.get_last_execution()
        if not execution:
            raise ValueError("No previous tool executions found")

        return [
            TextContent(
                type="text",
                text=json.dumps(
                    {
                        "id": execution.id,
                        "tool_name": execution.tool_name,
                        "command": execution.command,
                        "args": execution.args,
                        "exit_code": execution.exit_code,
                        "duration_seconds": round(execution.duration_seconds, 3),
                        "stdout": execution.stdout,
                        "stderr": execution.stderr,
                        "working_directory": execution.working_directory,
                        "timestamp": execution.timestamp,
                    },
                    indent=2,
                ),
            )
        ]

    @tool(
        name="get_runtime_estimate",
        description="Get runtime estimate for a tool based on historical data or configuration",
        input_schema={
            "type": "object",
            "properties": {
                "tool_name": {
                    "type": "string",
                    "description": "Name of the tool to estimate runtime for",
                }
            },
            "required": ["tool_name"],
        },
    )
    async def _handle_get_runtime_estimate(
        self, arguments: dict[str, Any]
    ) -> list[TextContent]:
        """Handle getting runtime estimate for a tool."""
        tool_name: str | None = arguments.get("tool_name")
        if not tool_name:
            raise ValueError("Missing required parameter: tool_name")

        tool_config = self.config.tools.get(tool_name)
        estimate: float = self.tool_runner.get_runtime_estimate(tool_name, tool_config)

        # Get history stats if available
        history: list[float] = self.tool_runner.runtime_history.get(tool_name, [])

        return [
            TextContent(
                type="text",
                text=json.dumps(
                    {
                        "tool_name": tool_name,
                        "estimated_runtime_seconds": round(estimate, 3),
                        "historical_runs": len(history),
                        "config_estimate": (
                            tool_config.expected_runtime_seconds
                            if tool_config
                            else None
                        ),
                        "using_historical_data": len(history) > 0,
                    },
                    indent=2,
                ),
            )
        ]

    @tool(
        name="list_tool_history",
        description="List recent executions with basic information",
        input_schema={
            "type": "object",
            "properties": {
                "limit": {
                    "type": "integer",
                    "description": "Maximum number of executions to return",
                    "default": 10,
                }
            },
        },
    )
    async def _handle_list_tool_history(
        self, arguments: dict[str, Any]
    ) -> list[TextContent]:
        """Handle listing recent tool executions."""
        limit: int = arguments.get("limit", 10)

        # Get recent executions sorted by timestamp
        executions = sorted(
            self.tool_runner.execution_cache.values(),
            key=lambda x: x.timestamp,
            reverse=True,
        )[:limit]

        history_data: list[dict[str, Any]] = []
        for execution in executions:
            history_data.append(
                {
                    "id": execution.id,
                    "tool_name": execution.tool_name,
                    "exit_code": execution.exit_code,
                    "duration_seconds": round(execution.duration_seconds, 3),
                    "timestamp": execution.timestamp,
                    "command": f"{execution.command} {' '.join(execution.args)}",
                }
            )

        return [
            TextContent(
                type="text",
                text=json.dumps(
                    {
                        "recent_executions": history_data,
                        "total_cached": len(self.tool_runner.execution_cache),
                    },
                    indent=2,
                ),
            )
        ]

    @tool(
        name="get_tool_config",
        description="Get the configuration for a specific tool",
        input_schema={
            "type": "object",
            "properties": {
                "tool_name": {
                    "type": "string",
                    "description": "Name of the tool to get configuration for",
                }
            },
            "required": ["tool_name"],
        },
    )
    async def _handle_get_tool_config(
        self, arguments: dict[str, Any]
    ) -> list[TextContent]:
        """Handle getting configuration for a specific tool."""
        tool_name: str | None = arguments.get("tool_name")
        if not tool_name:
            raise ValueError("Missing required parameter: tool_name")

        tool_config = self.config.tools.get(tool_name)
        if not tool_config:
            raise ValueError(f"Tool not found: {tool_name}")

        return [
            TextContent(
                type="text",
                text=json.dumps(
                    {
                        "name": tool_config.name,
                        "description": tool_config.description,
                        "command": tool_config.command,
                        "args": tool_config.args,
                        "expected_runtime_seconds": tool_config.expected_runtime_seconds,
                        "expected_output_size_bytes": tool_config.expected_output_size_bytes,
                        "working_directory": tool_config.working_directory,
                        "environment_variables": tool_config.environment_variables,
                        "timeout_seconds": tool_config.timeout_seconds,
                        "frozen_args": tool_config.frozen_args,
                    },
                    indent=2,
                ),
            )
        ]

    async def run(self) -> None:
        """Run the MCP server."""
        logger.info("Starting TDD MCP Server")
        logger.info(f"Loaded {len(self.config.tools)} tools from configuration")
        logger.info(f"Cache directory: {self.config.cache_directory}")

        # Clean up old cache entries
        self.tool_runner.cleanup_cache(self.config.max_history_entries)

        async with stdio_server() as (read_stream, write_stream):
            await self.server.run(
                read_stream,
                write_stream,
                InitializationOptions(
                    server_name="tdd-mcp-server",
                    server_version="0.1.0",
                    capabilities=self.server.get_capabilities(
                        notification_options=NotificationOptions(),
                        experimental_capabilities={},
                    ),
                ),
            )


def main() -> NoReturn:
    """Main entry point for the TDD MCP server."""

    os.chdir(os.environ["WORKSPACE_FOLDER_PATHS"])
    config_path: str | None = None
    if len(sys.argv) > 1:
        config_path = sys.argv[1]

    try:
        server: TDDMCPServer = TDDMCPServer(config_path)
        asyncio.run(server.run())
    except KeyboardInterrupt:
        logger.info("Server stopped by user")
        os.kill(os.getpid(), signal.SIGQUIT)
    except Exception as e:
        logger.error(f"Server error: {e}")
        sys.exit(1)
    sys.exit(0)


if __name__ == "__main__":
    main()
