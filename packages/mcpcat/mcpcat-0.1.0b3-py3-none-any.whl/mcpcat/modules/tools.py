"""Tool management and interception for MCPCat."""

from typing import Any, TYPE_CHECKING
from mcp.types import CallToolResult, TextContent
from mcpcat.modules.version_detection import has_fastmcp_support

from .logging import write_to_log

if TYPE_CHECKING or has_fastmcp_support():
    try:
        from mcp.server import FastMCP
    except ImportError:
        FastMCP = None

async def handle_report_missing(arguments: dict[str, Any]) -> CallToolResult:
    """Handle the report_missing tool."""
    missing_tool = arguments.get("missing_tool", "")
    description = arguments.get("description", "")


    # Log the report
    write_to_log(f"Missing tool reported: {missing_tool}, Description: {description}")

    return CallToolResult(
        content=[
            TextContent(
                type="text",
                text=f"Thank you for reporting that you need a '{missing_tool}' tool. This feedback helps improve the server."
            )
        ]
    )
