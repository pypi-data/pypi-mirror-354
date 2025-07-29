# MCP Jira Tools

## Installation (via PyPI)

Install the MCP Jira Tools package from PyPI:

```bash
pip install mcp-jira-tools
```

> If you use a virtual environment (recommended):
> ```bash
> python3 -m venv .venv
> source .venv/bin/activate
> pip install mcp-jira-tools
> ```

---

## Using with Cursor AI

1. **Register the MCP Server with Cursor**

   Add the following to your `~/.cursor/mcp.json` configuration file:

   ```json
   {
     "mcpServers": {
       "jira-mcp": {
         "command": "python",
         "args": ["-m", "mcp_jira_tools.server"],
         "env": {
           "JIRA_SERVER_URL": "https://your-jira-instance.com",
           "JIRA_TOKEN": "your_jira_token",
           "JIRA_PROJECT_KEY": "your-project"
         }
       }
     }
   }
   ```

2. **Start Cursor**

   - Open Cursor and ensure the MCP server is registered.
   - Jira tools will be available in the Cursor tool interface.

3. **No Session Management Needed**

   - Stdio transport is used; each Cursor session is a single process.
   - No session IDs or session-specific error messages are required.

---

## Overview
A FastMCP server that exposes tools for creating, updating, transitioning, searching, and retrieving Jira tickets. Designed for integration with Cursor AI using FastMCP's stdio transport.

---

## Features
- FastMCP server with Streamable HTTP transport
- Full Jira integration (create, update, transition, search, get tickets)
- Pydantic models for parameter validation
- Multiple configuration methods
- Secure credential management
- Comprehensive error handling
- Easy integration with Cursor AI

---

## Getting Started

### 1. Install Dependencies
```bash
pip install fastmcp jira pydantic
```

### 2. Configure Jira Settings
You can configure Jira settings in multiple ways:

#### A. Cursor MCP Configuration (Recommended)
Add Jira settings to your Cursor MCP configuration file (`~/.cursor/mcp.json`):
```json
{
  "mcpServers": {
    "jira-mcp": {
      "command": "python",
      "args": ["-m", "mcp_jira_tools.server"],
      "env": {
        "JIRA_SERVER_URL": "https://your-jira-instance.com",
        "JIRA_TOKEN": "your_jira_token",
        "JIRA_PROJECT_KEY": "your-project"
      }
    }
  }
}
```

This configuration:
- Defines a server named "jira-mcp"
- Runs the server using Python
- Sets Jira configuration via environment variables
- Cursor will automatically start the server when needed

#### B. Environment Variables
```bash
export JIRA_SERVER_URL="https://your-jira-instance.com"
export JIRA_TOKEN="your-token"
export JIRA_PROJECT_KEY="your-project"  # optional
```

#### C. Runtime Configuration
Use the `configure_jira` tool to set configuration at runtime:
```python
from fastmcp import FastMCP

mcp = FastMCP()
result = await mcp.invoke(
    "configure_jira",
    {
        "server_url": "https://your-jira-instance.com",
        "token": "your-token",
        "project_key": "your-project"
    }
)
```

### 3. Using the Tools

#### Example: Create a Ticket
```python
from fastmcp import FastMCP

mcp = FastMCP()
result = await mcp.invoke(
    "create_ticket",
    {
        "project": "PROJ",
        "summary": "Test issue",
        "description": "Created by test",
        "issuetype": "Task"
    }
)
```

#### Example: Search Tickets
```python
from fastmcp import FastMCP

mcp = FastMCP()
result = await mcp.invoke(
    "search_tickets",
    {
        "project": "PROJ",
        "status": "Open",
        "assignee": "currentUser()",
        "summary": "Test"
    }
)
```

### 4. Available Tools

#### Resource Endpoints
- `resource://jira/metadata` - Server metadata and supported operations
- `resource://jira/config` - Server configuration

#### Tool Endpoints
- `create_ticket` - Create a new Jira ticket
- `update_ticket` - Update an existing ticket
- `transition_ticket` - Change ticket status
- `search_tickets` - Search for tickets
- `get_ticket` - Get ticket details
- `configure_jira` - Configure Jira settings

### 5. Development

#### Project Structure
```
mcp-jira-tools/
├── mcp_jira_tools/
│   ├── __init__.py
│   ├── server.py         # FastMCP server and tool definitions
│   ├── jira_client.py    # Jira client abstraction
│   └── config.py         # Configuration management
├── tests/
│   ├── __init__.py
│   ├── test_mcp_jira_tools.py
│   └── mock_jira_server.py
├── requirements.txt
└── README.md
```

#### Running Tests
```bash
pytest tests/
```

#### Running the Server
```bash
python -m mcp_jira_tools.server
```

---

## Contributing
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests
5. Submit a pull request

---

## License
MIT License