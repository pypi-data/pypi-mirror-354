"""Tool execution and caching functionality for TDD MCP Server."""

from __future__ import annotations

import asyncio
import json
import os
import time
import uuid
from dataclasses import asdict, dataclass
from pathlib import Path

from tdd_mcp_server.config import ToolConfig


@dataclass
class ToolExecution:
    """Record of a tool execution."""

    id: str
    tool_name: str
    command: str
    args: list[str]
    exit_code: int
    duration_seconds: float
    stdout: str
    stderr: str
    timestamp: float
    working_directory: str | None = None


@dataclass
class QuietResult:
    """Quiet mode result with minimal information."""

    id: str
    exit_code: int
    duration_seconds: float


class ToolRunner:
    """Manages tool execution, caching, and runtime history."""

    def __init__(self, cache_directory: str = "~/.tdd-mcp-cache"):
        # Expand user directory and ensure absolute path
        expanded_path = os.path.expanduser(cache_directory)
        self.cache_directory = Path(expanded_path).resolve()

        # Create directory and any missing parent directories
        self.cache_directory.mkdir(parents=True, exist_ok=True)

        # Runtime history: tool_name -> list of durations
        self.runtime_history: dict[str, list[float]] = {}
        self.load_runtime_history()

        # Execution cache: id -> ToolExecution
        self.execution_cache: dict[str, ToolExecution] = {}
        self.load_execution_cache()

        # Track last execution for quick access
        self.last_execution_id: str | None = None

    def get_cache_file_path(self, filename: str) -> Path:
        """Get the full path for a cache file."""
        return self.cache_directory / filename

    def load_runtime_history(self) -> None:
        """Load runtime history from disk."""
        history_file = self.get_cache_file_path("runtime_history.json")
        if history_file.exists():
            try:
                with open(history_file, "r") as f:
                    self.runtime_history = json.load(f)
            except Exception:
                self.runtime_history = {}

    def save_runtime_history(self) -> None:
        """Save runtime history to disk."""
        history_file = self.get_cache_file_path("runtime_history.json")
        with open(history_file, "w") as f:
            json.dump(self.runtime_history, f, indent=2)

    def load_execution_cache(self) -> None:
        """Load execution cache from disk."""
        cache_file = self.get_cache_file_path("execution_cache.json")
        if cache_file.exists():
            try:
                with open(cache_file, "r") as f:
                    cache_data = json.load(f)
                    self.execution_cache = {
                        exec_id: ToolExecution(**exec_data)
                        for exec_id, exec_data in cache_data.items()
                    }
            except Exception:
                self.execution_cache = {}

    def save_execution_cache(self) -> None:
        """Save execution cache to disk."""
        cache_file = self.get_cache_file_path("execution_cache.json")
        cache_data = {
            exec_id: asdict(execution)
            for exec_id, execution in self.execution_cache.items()
        }
        with open(cache_file, "w") as f:
            json.dump(cache_data, f, indent=2)

    def add_runtime_record(self, tool_name: str, duration: float) -> None:
        """Add a runtime record for a tool."""
        if tool_name not in self.runtime_history:
            self.runtime_history[tool_name] = []

        self.runtime_history[tool_name].append(duration)

        # Keep only the last 100 records per tool to prevent unbounded growth
        if len(self.runtime_history[tool_name]) > 100:
            self.runtime_history[tool_name] = self.runtime_history[tool_name][-100:]

        self.save_runtime_history()

    def get_runtime_estimate(
        self, tool_name: str, tool_config: ToolConfig | None = None
    ) -> float:
        """Get runtime estimate for a tool based on history or config."""
        if tool_name in self.runtime_history and self.runtime_history[tool_name]:
            # Use historical average
            durations = self.runtime_history[tool_name]
            return sum(durations) / len(durations)
        elif tool_config:
            # Fall back to config estimate
            return tool_config.expected_runtime_seconds
        else:
            # Default estimate
            return 1.0

    async def run_tool(
        self,
        tool_config: ToolConfig,
        additional_args: list[str] | None = None,
        quiet: bool = True,
    ) -> tuple[QuietResult, ToolExecution | None]:
        """
        Run a tool and return the result.

        Args:
            tool_config: Configuration for the tool to run
            additional_args: Additional arguments to pass to the tool
            quiet: If True, return only minimal information

        Returns:
            Tuple of (QuietResult, full ToolExecution if not quiet)
        """
        execution_id = str(uuid.uuid4())

        # Prepare command and arguments
        full_args = tool_config.args.copy() + (additional_args or [])

        # Prepare environment
        env = os.environ.copy()
        if tool_config.environment_variables:
            env.update(tool_config.environment_variables)

        # Prepare working directory
        working_dir = tool_config.working_directory or os.getcwd()

        # Execute the command
        start_time = time.time()

        try:
            process = await asyncio.create_subprocess_exec(
                tool_config.command,
                *full_args,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
                env=env,
                cwd=working_dir,
            )

            # Wait for completion with timeout
            timeout = tool_config.timeout_seconds
            stdout_bytes, stderr_bytes = await asyncio.wait_for(
                process.communicate(), timeout=timeout
            )

            exit_code = process.returncode if process.returncode is not None else -1
            stdout = stdout_bytes.decode("utf-8", errors="replace")
            stderr = stderr_bytes.decode("utf-8", errors="replace")

        except asyncio.TimeoutError:
            # Kill the process if it times out
            try:
                process.kill()
                await process.wait()
            except (ProcessLookupError, PermissionError, OSError):
                pass

            exit_code = -1
            stdout = ""
            stderr = f"Command timed out after {timeout} seconds"

        except Exception as e:
            exit_code = -1
            stdout = ""
            stderr = f"Failed to execute command: {str(e)}"

        end_time = time.time()
        duration = end_time - start_time

        # Create execution record
        execution = ToolExecution(
            id=execution_id,
            tool_name=tool_config.name,
            command=tool_config.command,
            args=full_args,
            exit_code=exit_code,
            duration_seconds=duration,
            stdout=stdout,
            stderr=stderr,
            timestamp=start_time,
            working_directory=working_dir,
        )

        # Cache the execution
        self.execution_cache[execution_id] = execution
        self.last_execution_id = execution_id
        self.save_execution_cache()

        # Update runtime history
        self.add_runtime_record(tool_config.name, duration)

        # Create quiet result
        quiet_result = QuietResult(
            id=execution_id,
            exit_code=exit_code,
            duration_seconds=duration,
        )

        return quiet_result, execution if not quiet else None

    def get_execution(self, execution_id: str) -> ToolExecution | None:
        """Get a cached execution by ID."""
        return self.execution_cache.get(execution_id)

    def get_last_execution(self) -> ToolExecution | None:
        """Get the last executed tool's full result."""
        if self.last_execution_id:
            return self.execution_cache.get(self.last_execution_id)
        return None

    def cleanup_cache(self, max_entries: int = 1000) -> None:
        """Clean up old cache entries to prevent unbounded growth."""
        if len(self.execution_cache) > max_entries:
            # Sort by timestamp and keep only the most recent entries
            sorted_executions = sorted(
                self.execution_cache.items(), key=lambda x: x[1].timestamp, reverse=True
            )

            # Keep only the most recent entries
            self.execution_cache = dict(sorted_executions[:max_entries])
            self.save_execution_cache()
