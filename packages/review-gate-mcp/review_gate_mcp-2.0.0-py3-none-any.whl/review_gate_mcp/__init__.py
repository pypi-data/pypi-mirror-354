"""
Review Gate MCP Server - Modern implementation using FastMCP

A Model Context Protocol server that provides AI-powered code review and interaction tools.
Designed for integration with any MCP-compatible client.
"""

from importlib.metadata import version
from pathlib import Path

import tomllib

from review_gate_mcp.server import main, mcp


def _get_version() -> str:
    """Get version from package metadata or pyproject.toml"""
    try:
        return version("review-gate-mcp")
    except Exception:
        try:
            pyproject_path = Path(__file__).parent.parent.parent / "pyproject.toml"
            if pyproject_path.exists():
                with open(pyproject_path, "rb") as f:
                    data = tomllib.load(f)
                    return data.get("project", {}).get("version", "unknown")
        except Exception:
            return "unknown"
        return "unknown"


__version__ = _get_version()
__author__ = "Lakshman Turlapati, Abhishek Bhakat"
__email__ = "abhishek.bhakat@hotmail.com"

__all__ = ["main", "mcp"]
