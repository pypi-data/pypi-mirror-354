import os
import logging
import traceback
from typing import Dict, Any, Optional
from fastmcp import FastMCP
from pydantic import BaseModel, Field, ValidationError
from jira import JIRA
from dotenv import load_dotenv

# Set up logging with more detail
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

mcp = FastMCP("Jira MCP Server")

# Initialize Jira client
jira_client = None
if all(os.getenv(var) for var in ['JIRA_SERVER_URL', 'JIRA_TOKEN', 'JIRA_PROJECT_KEY']):
    try:
        jira_client = JIRA(
            server=os.getenv('JIRA_SERVER_URL'),
            token_auth=os.getenv('JIRA_TOKEN')
        )
        logger.info("Jira client initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize Jira client: {str(e)}")
        logger.error(traceback.format_exc())
else:
    logger.warning("Jira environment variables not set. Server will start without Jira connection.")

# Pydantic models for parameter validation
class CreateTicketParams(BaseModel):
    summary: str = Field(..., description="Summary of the ticket")
    description: str = Field(..., description="Description of the ticket")
    issue_type: str = Field(..., description="Type of the issue (e.g., Bug, Task)")
    priority: Optional[str] = Field(None, description="Priority of the ticket")

class UpdateTicketParams(BaseModel):
    ticket_id: str = Field(..., description="ID of the ticket to update")
    summary: Optional[str] = Field(None, description="New summary")
    description: Optional[str] = Field(None, description="New description")
    priority: Optional[str] = Field(None, description="New priority")
    assignee: Optional[str] = Field(None, description="Username or accountId to assign the ticket to")

class TransitionParams(BaseModel):
    ticket_id: str = Field(..., description="ID of the ticket to transition")
    transition_name: str = Field(..., description="Name of the transition (e.g., 'In Progress', 'Done')")

class SearchParams(BaseModel):
    jql: str = Field(..., description="JQL query string")
    max_results: int = Field(50, description="Maximum number of results to return")

class GetTicketParams(BaseModel):
    ticket_id: str = Field(..., description="ID of the ticket to retrieve")

class ConfigureParams(BaseModel):
    server_url: str = Field(..., description="Jira server URL")
    token: str = Field(..., description="Jira API token")
    project_key: str = Field(..., description="Jira project key")

def format_error_response(message, code=-32000, details=None):
    return {
        "error": {
            "code": code,
            "message": message,
            "details": details
        }
    }

# Resource definitions
@mcp.resource("resource://jira/metadata")
def metadata_resource() -> Dict[str, Any]:
    """Get metadata about the Jira integration."""
    return {
        "name": "Jira Integration",
        "version": "1.0.0",
        "description": "Integration with Jira for ticket management",
        "capabilities": [
            "create_ticket",
            "update_ticket",
            "transition_ticket",
            "search_tickets",
            "get_ticket",
            "configure_jira"
        ]
    }

@mcp.resource("resource://jira/config")
def config_resource() -> Dict[str, Any]:
    """Get current Jira configuration."""
    if not jira_client:
        return {"status": "not_configured"}
    return {
        "server_url": os.getenv("JIRA_SERVER_URL"),
        "project_key": os.getenv("JIRA_PROJECT_KEY"),
        "status": "configured"
    }

# Tool definitions
def _create_ticket_impl(params: CreateTicketParams):
    # Explicit validation for required fields
    if not params.summary or not params.description or not params.issue_type:
        raise ValueError("summary, description, and issue_type are required")
    if not jira_client:
        raise ValueError("Jira client not configured")
    issue_dict = {
        'project': {'key': os.getenv("JIRA_PROJECT_KEY")},
        'summary': params.summary,
        'description': params.description,
        'issuetype': {'name': params.issue_type},
    }
    if params.priority:
        issue_dict['priority'] = {'name': params.priority}
    new_issue = jira_client.create_issue(fields=issue_dict)
    return {
        "status": "success",
        "ticket_id": new_issue.key,
        "url": f"{os.getenv('JIRA_SERVER_URL')}/browse/{new_issue.key}"
    }

@mcp.tool("create_ticket")
def create_ticket(params: CreateTicketParams) -> Dict[str, Any]:
    try:
        return _create_ticket_impl(params)
    except ValidationError as ve:
        return format_error_response("Invalid parameters", code=-32602, details=ve.errors())
    except ValueError as ve:
        return format_error_response(str(ve), code=-32001)
    except Exception as e:
        logger.error(f"Error in create_ticket: {str(e)}")
        return format_error_response("Server error", code=-32000, details=str(e))

def _update_ticket_impl(params: UpdateTicketParams):
    if not jira_client:
        raise ValueError("Jira client not configured")
    issue = jira_client.issue(params.ticket_id)
    fields = {}
    if params.summary:
        fields['summary'] = params.summary
    if params.description:
        fields['description'] = params.description
    if params.priority:
        fields['priority'] = {'name': params.priority}
    if fields:
        issue.update(fields=fields)
    if params.assignee:
        jira_client.assign_issue(params.ticket_id, params.assignee)
    return {
        "status": "success",
        "ticket_id": params.ticket_id,
        "message": "Ticket updated successfully"
    }

@mcp.tool("update_ticket")
def update_ticket(params: UpdateTicketParams) -> Dict[str, Any]:
    try:
        return _update_ticket_impl(params)
    except ValidationError as ve:
        return format_error_response("Invalid parameters", code=-32602, details=ve.errors())
    except ValueError as ve:
        return format_error_response(str(ve), code=-32001)
    except Exception as e:
        logger.error(f"Error in update_ticket: {str(e)}")
        return format_error_response("Server error", code=-32000, details=str(e))

def _transition_ticket_impl(params: TransitionParams):
    if not jira_client:
        raise ValueError("Jira client not configured")
    issue = jira_client.issue(params.ticket_id)
    transitions = jira_client.transitions(issue)
    transition_id = None
    for t in transitions:
        if t['name'].lower() == params.transition_name.lower():
            transition_id = t['id']
            break
    if not transition_id:
        raise ValueError(f"Transition '{params.transition_name}' not found")
    jira_client.transition_issue(issue, transition_id)
    return {
        "status": "success",
        "ticket_id": params.ticket_id,
        "transition": params.transition_name
    }

@mcp.tool("transition_ticket")
def transition_ticket(params: TransitionParams) -> Dict[str, Any]:
    try:
        return _transition_ticket_impl(params)
    except ValidationError as ve:
        return format_error_response("Invalid parameters", code=-32602, details=ve.errors())
    except ValueError as ve:
        return format_error_response(str(ve), code=-32001)
    except Exception as e:
        logger.error(f"Error in transition_ticket: {str(e)}")
        return format_error_response("Server error", code=-32000, details=str(e))

def _search_tickets_impl(params: SearchParams):
    if not jira_client:
        raise ValueError("Jira client not configured")
    issues = jira_client.search_issues(
        params.jql,
        maxResults=params.max_results
    )
    return {
        "status": "success",
        "count": len(issues),
        "tickets": [
            {
                "id": issue.key,
                "summary": issue.fields.summary,
                "status": issue.fields.status.name,
                "url": f"{os.getenv('JIRA_SERVER_URL')}/browse/{issue.key}"
            }
            for issue in issues
        ]
    }

@mcp.tool("search_tickets")
def search_tickets(params: SearchParams) -> Dict[str, Any]:
    try:
        return _search_tickets_impl(params)
    except ValidationError as ve:
        return format_error_response("Invalid parameters", code=-32602, details=ve.errors())
    except ValueError as ve:
        return format_error_response(str(ve), code=-32001)
    except Exception as e:
        logger.error(f"Error in search_tickets: {str(e)}")
        return format_error_response("Server error", code=-32000, details=str(e))

def _get_ticket_impl(params: GetTicketParams):
    if not jira_client:
        raise ValueError("Jira client not configured")
    issue = jira_client.issue(params.ticket_id)
    assignee = None
    if issue.fields.assignee:
        assignee = {
            "name": issue.fields.assignee.displayName,
            "key": getattr(issue.fields.assignee, "key", None),
            "email": getattr(issue.fields.assignee, "emailAddress", None)
        }
    comments = [
        {
            "author": c.author.displayName,
            "body": c.body,
            "created": c.created
        }
        for c in getattr(issue.fields.comment, "comments", [])
    ]
    return {
        "status": "success",
        "ticket": {
            "id": issue.key,
            "summary": issue.fields.summary,
            "description": issue.fields.description,
            "status": issue.fields.status.name,
            "priority": issue.fields.priority.name if hasattr(issue.fields, 'priority') else None,
            "assignee": assignee,
            "comments": comments,
            "url": f"{os.getenv('JIRA_SERVER_URL')}/browse/{issue.key}"
        }
    }

@mcp.tool("get_ticket")
def get_ticket(params: GetTicketParams) -> Dict[str, Any]:
    try:
        return _get_ticket_impl(params)
    except ValidationError as ve:
        return format_error_response("Invalid parameters", code=-32602, details=ve.errors())
    except ValueError as ve:
        return format_error_response(str(ve), code=-32001)
    except Exception as e:
        logger.error(f"Error in get_ticket: {str(e)}")
        return format_error_response("Server error", code=-32000, details=str(e))

def _configure_jira_impl(params: ConfigureParams):
    global jira_client
    jira_client = JIRA(
        server=params.server_url,
        token_auth=params.token
    )
    os.environ['JIRA_SERVER_URL'] = params.server_url
    os.environ['JIRA_TOKEN'] = params.token
    os.environ['JIRA_PROJECT_KEY'] = params.project_key
    logger.info("Jira client configured successfully")
    return {
        "status": "success",
        "message": "Jira client configured successfully"
    }

@mcp.tool("configure_jira")
def configure_jira(params: ConfigureParams) -> Dict[str, Any]:
    try:
        return _configure_jira_impl(params)
    except ValidationError as ve:
        return format_error_response("Invalid parameters", code=-32602, details=ve.errors())
    except ValueError as ve:
        return format_error_response(str(ve), code=-32001)
    except Exception as e:
        logger.error(f"Error in configure_jira: {str(e)}")
        return format_error_response("Server error", code=-32000, details=str(e))

if __name__ == "__main__":
    mcp.run()