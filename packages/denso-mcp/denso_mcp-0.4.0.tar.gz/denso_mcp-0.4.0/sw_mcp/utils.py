import json
import logging
import os
from pathlib import Path
import platform
from typing import Any, Dict, List

from mcp import StdioServerParameters


# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def get_config_path():
    """Get the MCP server configuration path"""
    config_path = Path.cwd() / "server_config.json"

    if platform.system() != "Windows":
        raise EnvironmentError(
            "This utility is designed to work with Solidoworks on Windows only."
        )

    claude_config_path = (
        Path(os.environ.get("APPDATA", "")) / "Claude" / "claude_desktop_config.json"
    )

    if claude_config_path.exists():
        return claude_config_path

    if config_path.exists():
        return config_path

    raise FileNotFoundError(
        f"Configuration file not found at {config_path} or {claude_config_path}. "
        "Please ensure the MCP server configuration file exists."
    )


def load_claude_desktop_config() -> Dict[str, Any]:
    """Load Claude Desktop configuration"""

    try:
        config_path = get_config_path()
        file_text = config_path.read_text(encoding="utf-8")
        config = json.loads(file_text)
        return config
    except Exception as e:
        logger.error(f"Error loading config from {config_path}: {e}")
        return {}


def parse_mcp_servers_from_config() -> Dict[str, StdioServerParameters]:
    """Parse MCP server configurations from Claude Desktop config"""
    servers = {}
    config = load_claude_desktop_config()
    mcp_servers = config.get("mcpServers", {})

    for name, server_config in mcp_servers.items():
        try:
            command = server_config.get("command", "")
            args = server_config.get("args", [])
            env = server_config.get("env", {})

            if command:
                servers[name] = StdioServerParameters(
                    command=command, args=args, env=env
                )

        except Exception as e:
            logger.error(f"Error parsing server config for {name}: {e}")

    return servers
