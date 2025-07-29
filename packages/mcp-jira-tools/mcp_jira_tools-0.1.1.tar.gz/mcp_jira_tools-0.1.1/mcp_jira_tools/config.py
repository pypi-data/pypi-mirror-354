import os
import json
from typing import Optional
from pathlib import Path

class JiraConfig:
    def __init__(self):
        self.server_url: Optional[str] = os.getenv("JIRA_SERVER_URL")
        self.token: Optional[str] = os.getenv("JIRA_TOKEN")
        self.project_key: Optional[str] = os.getenv("JIRA_PROJECT_KEY")
        
        # Try to read from Cursor's mcp.json
        self._load_from_cursor_config()

    def _load_from_cursor_config(self):
        """Load Jira configuration from Cursor's mcp.json if available."""
        cursor_config_path = Path.home() / ".cursor" / "mcp.json"
        if cursor_config_path.exists():
            try:
                with open(cursor_config_path) as f:
                    config = json.load(f)
                    for server in config.get("servers", []):
                        if server.get("name") == "Jira MCP Server":
                            # Get Jira settings from server config
                            jira_config = server.get("jira", {})
                            if not self.server_url and "server_url" in jira_config:
                                self.server_url = jira_config["server_url"]
                            if not self.project_key and "project_key" in jira_config:
                                self.project_key = jira_config["project_key"]
                            break
            except Exception as e:
                print(f"Warning: Could not read Cursor MCP config: {e}")

    def get_server_url(self) -> str:
        if not self.server_url:
            raise ValueError("JIRA_SERVER_URL environment variable is not set")
        return self.server_url

    def get_token(self) -> str:
        if not self.token:
            raise ValueError("JIRA_TOKEN environment variable is not set")
        return self.token

    def get_project_key(self) -> Optional[str]:
        return self.project_key

# Global configuration instance
config = JiraConfig() 