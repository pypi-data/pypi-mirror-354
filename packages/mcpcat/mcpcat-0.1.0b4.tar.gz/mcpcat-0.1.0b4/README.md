# MCPCat Python SDK

Analytics tool for MCP (Model Context Protocol) servers that provides insights into tool usage patterns.

## Features

- **Tool Usage Analytics**: Tracks which tools are called and how frequently
- **Context Injection**: Adds context parameters to tools to understand user intent  
- **Session Tracking**: Identifies and tracks user sessions
- **Report Missing Tools**: Allows clients to report when needed tools are missing
- **PII Redaction**: Automatically redacts sensitive information from logs
- **Non-invasive Integration**: Simple one-line integration with existing MCP servers

## Compatibility
MCPCat officially supports >=v1.2.0 of the Python SDK. Support for >=1.0.0 is experimental.

## Installation

```bash
pip install mcpcat
```

## Quick Start

```python
from fastmcp import FastMCP
from mcpcat import track

# Create your MCP server
mcp = FastMCP("my-server")

# Add your tools
@mcp.tool()
def my_tool(arg: str) -> str:
    return f"Result: {arg}"

# Enable MCPCat tracking
track(mcp)

# Run the server
mcp.run()
```

## Configuration

MCPCat can be configured with various options:

```python
from mcpcat import track, MCPCatOptions

options = MCPCatOptions(
    enable_tool_context=True,   # Add context parameters to tools
    enable_tracing=True,           # Trace tool calls
    enable_report_missing=True,     # Add report_missing tool
    identify=my_identify_func     # Custom session identification
)

track(mcp, options)
```

## How It Works

1. MCPCat intercepts the MCP server's tool listing and calling mechanisms
2. It injects a `context` parameter into each tool's schema
3. When tools are called, it captures analytics data including timing, arguments, and results
4. The `report_missing` tool allows LLMs to report when they need functionality that isn't available

## Custom Session Identification

You can provide a custom function to identify users:

```python
def identify_user(request_context):
    # Your logic to identify the user
    return {
        "sessionId": "session-123",
        "userId": "user-456"
    }

options = MCPCatOptions(identify=identify_user)
```

## Log Format

MCPCat logs are written in JSON format with the following structure:

```json
{
  "timestamp": "2024-01-20T10:30:00Z",
  "event": "tool_call",
  "tool_name": "my_tool",
  "session_id": "session-123",
  "user_id": "user-456",
  "duration": 0.123,
  "result": "success",
  "context_provided": true
}
```

## Development

To set up for development:

```bash
# Clone the repository
git clone https://github.com/yourusername/mcpcat-python-sdk.git
cd mcpcat-python-sdk

# Install dependencies
pip install -e ".[dev]"

# Run tests
pytest

# Run type checking
mypy src

# Run linting
ruff check src
```

## License

MIT