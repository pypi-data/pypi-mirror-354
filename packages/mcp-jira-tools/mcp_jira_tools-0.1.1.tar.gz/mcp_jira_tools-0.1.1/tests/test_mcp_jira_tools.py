import pytest
from unittest.mock import patch, MagicMock
from mcp_jira_tools import server

# Test data
TEST_TICKET_KEY = "PROJ-123"

@pytest.fixture
def mock_jira():
    with patch('mcp_jira_tools.server.jira_client') as mock_jira:
        yield mock_jira

# Create Ticket
def test_create_ticket_success(mock_jira):
    mock_issue = MagicMock()
    mock_issue.key = TEST_TICKET_KEY
    mock_jira.create_issue.return_value = mock_issue
    params = server.CreateTicketParams(
        summary='Test', description='Desc', issue_type='Task', priority=None
    )
    result = server._create_ticket_impl(params)
    assert result['status'] == 'success'
    assert result['ticket_id'] == TEST_TICKET_KEY

# Update Ticket
def test_update_ticket_success(mock_jira):
    mock_issue = MagicMock()
    mock_jira.issue.return_value = mock_issue
    params = server.UpdateTicketParams(
        ticket_id=TEST_TICKET_KEY, summary='Updated', description=None, priority=None, assignee=None
    )
    result = server._update_ticket_impl(params)
    assert result['status'] == 'success'
    assert result['ticket_id'] == TEST_TICKET_KEY

# Transition Ticket
def test_transition_ticket_success(mock_jira):
    mock_issue = MagicMock()
    mock_jira.issue.return_value = mock_issue
    mock_jira.transitions.return_value = [{'name': 'In Progress', 'id': '21'}]
    params = server.TransitionParams(
        ticket_id=TEST_TICKET_KEY, transition_name='In Progress'
    )
    result = server._transition_ticket_impl(params)
    assert result['status'] == 'success'
    assert result['ticket_id'] == TEST_TICKET_KEY
    assert result['transition'] == 'In Progress'

# Search Tickets
def test_search_tickets_success(mock_jira):
    mock_issue = MagicMock()
    mock_issue.key = TEST_TICKET_KEY
    mock_issue.fields.summary = 'Test Issue'
    mock_issue.fields.status.name = 'To Do'
    mock_jira.search_issues.return_value = [mock_issue]
    params = server.SearchParams(jql='project=PROJ', max_results=10)
    result = server._search_tickets_impl(params)
    assert result['status'] == 'success'
    assert result['count'] == 1
    assert result['tickets'][0]['id'] == TEST_TICKET_KEY

# Get Ticket
def test_get_ticket_success(mock_jira):
    mock_issue = MagicMock()
    mock_issue.key = TEST_TICKET_KEY
    mock_issue.fields.summary = 'Test Issue'
    mock_issue.fields.description = 'Test Description'
    mock_issue.fields.status.name = 'To Do'
    mock_issue.fields.priority.name = 'High'
    mock_issue.fields.assignee.displayName = 'Test User'
    mock_issue.fields.assignee.key = 'userkey'
    mock_issue.fields.assignee.emailAddress = 'test@example.com'
    mock_issue.fields.comment.comments = []
    mock_jira.issue.return_value = mock_issue
    params = server.GetTicketParams(ticket_id=TEST_TICKET_KEY)
    result = server._get_ticket_impl(params)
    assert result['status'] == 'success'
    assert result['ticket']['id'] == TEST_TICKET_KEY
    assert result['ticket']['assignee']['name'] == 'Test User'

# Configure Jira
def test_configure_jira_success(mock_jira):
    from unittest.mock import patch, MagicMock
    with patch('mcp_jira_tools.server.JIRA') as mock_jira_class:
        mock_jira_class.return_value = MagicMock()
        params = server.ConfigureParams(
            server_url='https://jira.example.com',
            token='token',
            project_key='PROJ'
        )
        result = server._configure_jira_impl(params)
        assert result['status'] == 'success'

# Error Handling: Create Ticket with Invalid Params
def test_create_ticket_invalid_params(mock_jira):
    params = server.CreateTicketParams(
        summary='', description='', issue_type='', priority=None
    )
    # Simulate ValidationError by raising it in the function if needed
    try:
        result = server._create_ticket_impl(params)
    except Exception as e:
        result = {"error": str(e)}
    assert 'error' in result

# Error Handling: Update Ticket with Jira client not configured
def test_update_ticket_no_jira():
    with patch('mcp_jira_tools.server.jira_client', None):
        params = server.UpdateTicketParams(
            ticket_id=TEST_TICKET_KEY, summary='Updated', description=None, priority=None, assignee=None
        )
        try:
            result = server._update_ticket_impl(params)
        except Exception as e:
            result = {"error": str(e)}
        assert 'error' in result 