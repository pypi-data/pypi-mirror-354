import os
from jira import JIRA

class JiraClient:
    def __init__(self):
        self.server_url = os.getenv("JIRA_SERVER_URL")
        self.token = os.getenv("JIRA_TOKEN")
        self.project_key = os.getenv("JIRA_PROJECT_KEY")
        if not self.server_url or not self.token:
            raise ValueError("JIRA_SERVER_URL and JIRA_TOKEN must be set in environment variables.")
        self.jira = JIRA(server=self.server_url, token_auth=self.token)

    def get_ticket(self, ticket_id):
        return self.jira.issue(ticket_id)

    def search_tickets(self, jql, max_results=50):
        return self.jira.search_issues(jql, maxResults=max_results) 