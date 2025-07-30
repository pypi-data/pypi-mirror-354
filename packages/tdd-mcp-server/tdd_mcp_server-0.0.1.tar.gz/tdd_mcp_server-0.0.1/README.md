# TDD MCP Server

A Model Context Protocol (MCP) server designed for test-driven development workflows. This server allows you to register command-line tools in a configuration file and execute them through MCP, with features like output caching, runtime estimation, and quiet mode execution.

## Features

- **Configurable Tools**: Define any command-line tool in `tdd-mcp-config.toml`
- **Flexible Configuration**: Support for custom arguments, working directories, environment variables, and timeouts
- **Runtime Estimation**: Tracks historical execution times, allowing agent to call cheap tools many times and only prefer expensive ones when necessary
- **Context window efficient**: Tools run in quiet mode by default, returning only execution ID, exit code, and duration, with full output available on agent request

## Installation

```bash
pip install tdd-mcp-server
```

## Quick Start

1. **Initialize configuration**:
   ```bash
   tdd-mcp-server init
   ```

2. **Edit the configuration** (`tdd-mcp-config.toml`) to add your tools

3. **Add the MCP server to your cursor config** (`.cursor/mcp.json`):
   ```
   {
     "mcpServers": {
       "tdd-mcp-server": {
         "command": "/venv/path/to/bin/tdd-mcp-server",  // example: ~/.virtualenvs/tdd-mcp-server/bin/tdd-mcp-server
         "args": ["--config", "tdd-mcp-config.toml", "run"]
       }
     }
   }
   ```
   
...or, simply run it standalone:
   ```bash
   tdd-mcp-server run
   ```

## Configuration

The server is configured via a TOML file (by default `tdd-mcp-config.toml`). Here's an example:

```toml
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

[tools.mypy]
description = "Run Python type checking with mypy"
command = "mypy"
args = ["."]
expected_runtime_seconds = 8.0
expected_output_size_bytes = 2048
working_directory = "."
timeout_seconds = 60.0

[tools.security_scan]
description = "Run security vulnerability scan"
command = "safety"
args = ["check", "--json"]
expected_runtime_seconds = 5.0
expected_output_size_bytes = 2048
working_directory = "."
timeout_seconds = 60.0
frozen_args = true  # Prevents agents from changing scan parameters
```

### Tool Configuration Options

- `description`: Human-readable description of what the tool does
- `command`: The executable command to run
- `args`: Default arguments to pass to the command
- `expected_runtime_seconds`: Estimated runtime (used for planning)
- `expected_output_size_bytes`: Estimated output size
- `working_directory`: Directory to run the command in (optional)
- `environment_variables`: Additional environment variables (optional)
- `timeout_seconds`: Maximum time to allow the command to run (optional)
- `frozen_args`: If true, prevents agents from providing alternative arguments (optional, default: false)

### Frozen Arguments

The `frozen_args` option allows you to lock down the arguments for specific tools, preventing AI agents from modifying them. This is useful for:

- **Security tools**: Ensure security scans run with specific, audited parameters
- **Critical operations**: Prevent accidental modification of important build or deployment commands  
- **Compliance**: Maintain consistent tool execution for regulatory requirements
- **Production safety**: Lock configuration for tools that affect production systems

When `frozen_args = true`:
- The tool's MCP schema will not include an `args` parameter
- Any additional arguments passed by the agent will be ignored
- Only the pre-configured `args` from the TOML file will be used

Example use cases:
```toml
[tools.security_audit]
command = "bandit"
args = ["-r", ".", "-f", "json", "-ll"]
frozen_args = true  # Security audit must use exact parameters

[tools.production_deploy]
command = "kubectl"
args = ["apply", "-f", "prod-config.yaml", "--dry-run=server"]
frozen_args = true  # Deployment commands cannot be modified
```

## Available MCP Tools

### Configured Tools
Each tool you define in the configuration becomes available as an MCP tool with these parameters:
- `args` (optional): Additional arguments to pass to the tool
- `quiet` (default: true): Whether to return minimal output

### Utility Tools

#### `get_output_for_tool_call_id`
Retrieve the full output for a specific execution:
```json
{
  "id": "uuid-of-execution"
}
```

#### `get_last_tool_call_output`
Retrieve the full output for the most recent execution:
```json
{}
```

#### `get_runtime_estimate`
Get runtime estimate for a tool:
```json
{
  "tool_name": "pytest"
}
```

#### `list_tool_history`
List recent executions:
```json
{
  "limit": 10
}
```

#### `get_tool_config`
Get configuration for a specific tool:
```json
{
  "tool_name": "pytest"
}
```

## Usage Patterns

### Typical TDD Workflow

1. **Run tests in quiet mode** (default behavior):
   ```json
   {
     "tool": "pytest",
     "arguments": {}
   }
   ```
   Returns: `{"id": "uuid", "exit_code": 1, "duration_seconds": 2.34, "status": "failure"}`

2. **Get full output for failed tests**:
   ```json
   {
     "tool": "get_output_for_tool_call_id",
     "arguments": {"id": "uuid"}
   }
   ```
   Returns full stdout/stderr to analyze failures

3. **Check runtime estimates** before running expensive tools:
   ```json
   {
     "tool": "get_runtime_estimate",
     "arguments": {"tool_name": "mypy"}
   }
   ```

### Custom Arguments

You can pass additional arguments to any tool:
```json
{
  "tool": "pytest",
  "arguments": {
    "args": ["tests/test_specific.py", "-k", "test_function"],
    "quiet": false
  }
}
```

## CLI Commands

### `tdd-mcp-server init`
Create a new configuration file with example tools.

Options:
- `--force, -f`: Overwrite existing configuration
- `--config, -c`: Specify config file path

### `tdd-mcp-server validate`
Validate the configuration file.

### `tdd-mcp-server list-tools`
Show all configured tools and their settings.

### `tdd-mcp-server run`
Start the MCP server.

## File Structure

```
.tdd-mcp-cache/           # Cache directory
├── execution_cache.json  # Cached command outputs
└── runtime_history.json  # Historical runtime data

tdd-mcp-config.toml       # Main configuration file
```

## Integration with AI Assistants

This MCP server is designed to work with AI assistants that support the Model Context Protocol. The assistant can:

1. Run tests and other tools in quiet mode for quick feedback
2. Only request full output when there are failures (non-zero exit codes)
3. Use runtime estimates to make informed decisions about which tools to run
4. Build up historical data to improve estimates over time

## Example Use Cases

- **Python Projects**: pytest, mypy, black, ruff, coverage
- **JavaScript/TypeScript**: npm test, jest, eslint, tsc, prettier
- **Rust**: cargo test, cargo check, cargo clippy, cargo fmt
- **Go**: go test, go vet, go fmt, golint
- **Multi-language**: running language-specific tools based on file changes

## Security Considerations

- The server executes arbitrary commands defined in the configuration
- Only use this with trusted configuration files
- Consider running in a containerized environment for additional isolation
- Review all tool configurations before deployment

## Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues for bugs and feature requests.

## License

BSD 3 Clause License - see LICENSE file for details. 
