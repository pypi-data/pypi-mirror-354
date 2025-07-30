import pytest
from mcp_bugbot_gitlab.resources import _post_aggregated_findings_to_gitlab_impl

def test_post_aggregated_findings_to_gitlab(monkeypatch):
    state = {
        "state": "approved",
        "findings": [
            {"file": "main.py", "line": 1, "message": "Null pointer.", "suggestion": "Add null check."}
        ],
        "summary": "Test summary."
    }
    # Mock get_review_state
    monkeypatch.setattr("mcp_bugbot_gitlab.resources.get_review_state", lambda p, m: state)
    # Mock GitLab client
    class MockNote:
        def __init__(self, id):
            self.id = id
    class MockGitLabClient:
        def post_comment(self, project_id, mr_iid, body):
            return MockNote(id=42)
    monkeypatch.setattr("mcp_bugbot_gitlab.resources.get_gitlab_client", lambda: MockGitLabClient())
    # Run tool
    result = _post_aggregated_findings_to_gitlab_impl({"project_id": "test", "mr_iid": 1})
    assert any(r["type"] == "summary" for r in result["results"])
    assert any(r.get("file") == "main.py" for r in result["results"]) 