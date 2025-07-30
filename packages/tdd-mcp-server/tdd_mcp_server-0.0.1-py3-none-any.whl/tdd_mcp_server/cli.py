"""Command-line interface for TDD MCP Server management."""

import argparse
import os
import sys
from typing import NoReturn

from tdd_mcp_server.config import create_example_config, load_config


def cmd_init(args: argparse.Namespace) -> int:
    """Initialize a new TDD MCP configuration."""
    config_path: str = args.config or "tdd-mcp-config.toml"

    if os.path.exists(config_path) and not args.force:
        print(
            f"Configuration file {config_path} already exists. Use --force to overwrite."
        )
        return 1

    create_example_config(config_path)
    print(f"Created example configuration at {config_path}")
    print("Edit this file to configure your TDD tools.")
    return 0


def cmd_validate(args: argparse.Namespace) -> int:
    """Validate a TDD MCP configuration file."""
    config_path: str = args.config

    try:
        config = load_config(config_path)
        print("Configuration is valid!")
        print(f"Found {len(config.tools)} tools:")
        for tool_name in config.tools:
            print(f"  - {tool_name}")
        return 0
    except Exception as e:
        print(f"Configuration validation failed: {e}")
        return 1


def cmd_list_tools(args: argparse.Namespace) -> int:
    """List all configured tools."""
    config_path: str = args.config

    try:
        config = load_config(config_path)
        if not config.tools:
            print("No tools configured.")
            return 0

        print("Configured tools:")
        for tool_name, tool_config in config.tools.items():
            print(f"\n{tool_name}:")
            print(f"  Description: {tool_config.description}")
            print(f"  Command: {tool_config.command} {' '.join(tool_config.args)}")
            print(f"  Expected runtime: {tool_config.expected_runtime_seconds}s")
            print(f"  Working directory: {tool_config.working_directory or 'current'}")
            if tool_config.timeout_seconds:
                print(f"  Timeout: {tool_config.timeout_seconds}s")
            if tool_config.frozen_args:
                print("  Args: frozen (cannot be overridden)")
            else:
                print("  Args: configurable")

        return 0
    except Exception as e:
        print(f"Failed to load configuration: {e}")
        return 1


def cmd_run_server(args: argparse.Namespace) -> NoReturn:
    """Run the TDD MCP server."""
    from tdd_mcp_server.server import main as server_main

    # Set config path in sys.argv for the server
    if args.config:
        sys.argv = ["tdd-mcp-server", args.config]
    else:
        sys.argv = ["tdd-mcp-server"]

    server_main()


def cmd_link_rules(args: argparse.Namespace) -> int:
    """Create a symlink from .cursor/rules to the tdd-mcp-server.mdc file."""
    try:
        # Try modern importlib.resources first (Python 3.9+)
        try:
            from importlib.resources import files

            mdc_path: str = str(files("tdd_mcp_server") / "tdd-mcp-server.mdc")
        except ImportError:
            # Fallback to pkg_resources for older Python versions
            import pkg_resources

            mdc_path = pkg_resources.resource_filename(
                "tdd_mcp_server", "tdd-mcp-server.mdc"
            )
    except (ImportError, FileNotFoundError, Exception):
        # Fallback for development mode - look for the file in the current directory
        current_dir: str = os.getcwd()
        mdc_path = os.path.join(current_dir, "tdd-mcp-server.mdc")
        if not os.path.exists(mdc_path):
            print("Error: tdd-mcp-server.mdc file not found")
            return 1

    # Create .cursor directory if it doesn't exist
    cursor_dir: str = os.path.join(os.getcwd(), ".cursor")
    rules_dir: str = os.path.join(cursor_dir, "rules")

    os.makedirs(rules_dir, exist_ok=True)

    # Create the symlink
    target_link: str = os.path.join(rules_dir, "tdd-mcp-server.mdc")

    # Remove existing symlink/file if it exists
    if os.path.exists(target_link) or os.path.islink(target_link):
        if (
            args.force
            or input(f"File {target_link} already exists. Overwrite? (y/N): ").lower()
            == "y"
        ):
            os.remove(target_link)
        else:
            print("Operation cancelled.")
            return 1

    try:
        os.symlink(mdc_path, target_link)
        print(f"Created symlink: {target_link} -> {mdc_path}")
        return 0
    except OSError as e:
        print(f"Failed to create symlink: {e}")
        return 1


def main() -> int:
    """Main CLI entry point."""
    # Check if we're in a virtual environment and activate if needed
    venv_path: str | None = os.environ.get("VIRTUAL_ENV")
    if not venv_path:
        # Check if sys.executable is in a virtual environment path
        executable_dir: str = os.path.dirname(os.path.dirname(sys.executable))

        if any(venv_dir in executable_dir for venv_dir in [".venv", ".virtualenvs"]):
            venv_path = executable_dir
        # Check if there's an activate script in the same directory
        elif os.path.exists(os.path.join(executable_dir, "bin", "activate")):
            venv_path = executable_dir

    if venv_path:
        activate_script: str = os.path.join(venv_path, "bin", "activate")
        executable_path: str = os.path.join(venv_path, "bin", "tdd-mcp-server")
        if os.path.exists(activate_script) and not os.getenv("VIRTUAL_ENV"):
            bash_cmd: str = (
                f"source {activate_script} && {executable_path} {' '.join(sys.argv[1:])}"
            )
            print("running", bash_cmd, file=sys.stderr)
            os.execvp("bash", ["bash", "-c", bash_cmd])

    parser: argparse.ArgumentParser = argparse.ArgumentParser(
        description="TDD MCP Server - Test-driven development tools via MCP"
    )
    parser.add_argument(
        "--config",
        "-c",
        default="tdd-mcp-config.toml",
        help="Path to configuration file",
    )

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # init command
    init_parser: argparse.ArgumentParser = subparsers.add_parser(
        "init", help="Initialize a new configuration"
    )
    init_parser.add_argument(
        "--force", "-f", action="store_true", help="Overwrite existing configuration"
    )

    # validate command
    subparsers.add_parser("validate", help="Validate configuration")

    # list-tools command
    subparsers.add_parser("list-tools", help="List configured tools")

    # run command
    subparsers.add_parser("run", help="Run the MCP server")

    # link-rules command
    link_rules_parser: argparse.ArgumentParser = subparsers.add_parser(
        "link-rules", help="Create symlink from .cursor/rules to tdd-mcp-server.mdc"
    )
    link_rules_parser.add_argument(
        "--force",
        "-f",
        action="store_true",
        help="Overwrite existing symlink without prompting",
    )

    args: argparse.Namespace = parser.parse_args()

    if args.command == "init":
        return cmd_init(args)
    elif args.command == "validate":
        return cmd_validate(args)
    elif args.command == "list-tools":
        return cmd_list_tools(args)
    elif args.command == "run":
        return cmd_run_server(args)
    elif args.command == "link-rules":
        return cmd_link_rules(args)
    else:
        parser.print_help()
        return 1


if __name__ == "__main__":
    sys.exit(main())
