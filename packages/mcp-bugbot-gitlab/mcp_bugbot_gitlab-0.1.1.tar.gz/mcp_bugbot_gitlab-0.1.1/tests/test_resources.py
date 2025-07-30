import pytest
from mcp_bugbot_gitlab.resources import _preview_review_findings_impl

def test_preview_review_findings(monkeypatch):
    state = {
        "findings": [
            {"type": "bug", "severity": "high", "file": "main.py", "line": 1, "message": "Null pointer."}
        ],
        "suggestion": "approve",
        "state": "approved",
        "summary": "Test summary."
    }
    monkeypatch.setattr("mcp_bugbot_gitlab.resources.get_review_state", lambda p, m: state)
    result = _preview_review_findings_impl({"project_id": "test", "mr_iid": 1})
    assert result["findings"] == state["findings"]
    assert result["suggestion"] == "approve"
    assert result["state"] == "approved" 