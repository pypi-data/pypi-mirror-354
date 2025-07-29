import aiohttp
from typing import Dict, List, Optional
from pydantic import BaseModel

class JiraClient:
    def __init__(self, server_url: str, token: str, project_key: Optional[str] = None):
        self.server_url = server_url.rstrip('/')
        self.token = token
        self.project_key = project_key
        self.headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
            "Accept": "application/json"
        }

    async def _request(self, method: str, endpoint: str, **kwargs) -> Dict:
        """Make a request to the Jira API."""
        url = f"{self.server_url}{endpoint}"
        async with aiohttp.ClientSession() as session:
            async with session.request(method, url, headers=self.headers, **kwargs) as response:
                if response.status >= 400:
                    error_text = await response.text()
                    raise Exception(f"Jira API error: {error_text}")
                return await response.json()

    async def create_ticket(self, project: str, summary: str, description: str, issuetype: str) -> Dict:
        """Create a new Jira ticket."""
        data = {
            "fields": {
                "project": {"key": project},
                "summary": summary,
                "description": description,
                "issuetype": {"name": issuetype}
            }
        }
        return await self._request("POST", "/rest/api/2/issue", json=data)

    async def update_ticket(self, issue_key: str, fields: Dict) -> Dict:
        """Update an existing Jira ticket."""
        data = {"fields": fields}
        return await self._request("PUT", f"/rest/api/2/issue/{issue_key}", json=data)

    async def transition_ticket(self, issue_key: str, transition: str) -> Dict:
        """Transition a Jira ticket to a new status."""
        data = {"transition": {"name": transition}}
        return await self._request("POST", f"/rest/api/2/issue/{issue_key}/transitions", json=data)

    async def search_tickets(self, project: Optional[str] = None, status: Optional[str] = None,
                           assignee: Optional[str] = None, summary: Optional[str] = None) -> List[Dict]:
        """Search for Jira tickets."""
        data = {
            "project": project,
            "status": status,
            "assignee": assignee,
            "summary": summary
        }
        response = await self._request("POST", "/rest/api/2/search", json=data)
        return response.get("issues", [])

    async def get_ticket(self, issue_key: str) -> Dict:
        """Get a Jira ticket by key."""
        return await self._request("GET", f"/rest/api/2/issue/{issue_key}") 