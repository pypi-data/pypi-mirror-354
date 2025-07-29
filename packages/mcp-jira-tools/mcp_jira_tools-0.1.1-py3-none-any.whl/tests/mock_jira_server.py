from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, List, Optional
import uvicorn
import asyncio
from datetime import datetime

app = FastAPI()

# Mock data store
tickets = {}
next_id = 1

# Models
class Status(BaseModel):
    name: str

class IssueType(BaseModel):
    name: str

class Project(BaseModel):
    key: str

class Fields(BaseModel):
    summary: str
    description: str
    status: Status
    issuetype: IssueType
    project: Project

class Ticket(BaseModel):
    id: str
    key: str
    fields: Fields

class CreateTicketRequest(BaseModel):
    project: str
    summary: str
    description: str
    issuetype: str

class UpdateTicketRequest(BaseModel):
    fields: Dict

class TransitionRequest(BaseModel):
    transition: str

class SearchRequest(BaseModel):
    project: Optional[str] = None
    status: Optional[str] = None
    assignee: Optional[str] = None
    summary: Optional[str] = None

# Routes
@app.post("/rest/api/2/issue")
async def create_ticket(request: CreateTicketRequest):
    global next_id
    ticket_id = f"{request.project}-{next_id}"
    next_id += 1
    
    ticket = Ticket(
        id=ticket_id,
        key=ticket_id,
        fields=Fields(
            summary=request.summary,
            description=request.description,
            status=Status(name="To Do"),
            issuetype=IssueType(name=request.issuetype),
            project=Project(key=request.project)
        )
    )
    
    tickets[ticket_id] = ticket
    return ticket

@app.get("/rest/api/2/issue/{issue_key}")
async def get_ticket(issue_key: str):
    if issue_key not in tickets:
        raise HTTPException(status_code=404, detail="Ticket not found")
    return tickets[issue_key]

@app.put("/rest/api/2/issue/{issue_key}")
async def update_ticket(issue_key: str, request: UpdateTicketRequest):
    if issue_key not in tickets:
        raise HTTPException(status_code=404, detail="Ticket not found")
    
    ticket = tickets[issue_key]
    for field, value in request.fields.items():
        if hasattr(ticket.fields, field):
            setattr(ticket.fields, field, value)
    
    return ticket

@app.post("/rest/api/2/issue/{issue_key}/transitions")
async def transition_ticket(issue_key: str, request: TransitionRequest):
    if issue_key not in tickets:
        raise HTTPException(status_code=404, detail="Ticket not found")
    
    ticket = tickets[issue_key]
    ticket.fields.status.name = request.transition
    return ticket

@app.post("/rest/api/2/search")
async def search_tickets(request: SearchRequest):
    results = []
    for ticket in tickets.values():
        if request.project and ticket.fields.project.key != request.project:
            continue
        if request.status and ticket.fields.status.name != request.status:
            continue
        if request.summary and request.summary.lower() not in ticket.fields.summary.lower():
            continue
        results.append(ticket)
    
    return {"issues": results}

def start_mock_server():
    """Start the mock Jira server."""
    uvicorn.run(app, host="127.0.0.1", port=8080)

def reset_mock_data():
    """Reset the mock data store."""
    global tickets, next_id
    tickets = {}
    next_id = 1

if __name__ == "__main__":
    start_mock_server() 