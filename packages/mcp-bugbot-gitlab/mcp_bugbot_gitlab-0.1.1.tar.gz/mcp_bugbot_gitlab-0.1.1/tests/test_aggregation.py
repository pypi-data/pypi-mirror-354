import pytest
from mcp_bugbot_gitlab.resources import _aggregate_review_findings_impl

def test_aggregate_review_findings_dedup(monkeypatch):
    # Mock state with duplicate findings
    state = {
        "chunk_review_progress": {
            "file1.py": [
                {"type": "bug", "severity": "high", "file": "file1.py", "line": 10, "message": "Null pointer."},
                {"type": "bug", "severity": "high", "file": "file1.py", "line": 10, "message": "Null pointer."}
            ],
            "file2.py": [
                {"type": "suggestion", "severity": "low", "file": "file2.py", "line": 5, "message": "Add docstring."}
            ]
        }
    }
    # Patch get_review_state and save_review_state
    monkeypatch.setattr("mcp_bugbot_gitlab.resources.get_review_state", lambda p, m: state)
    monkeypatch.setattr("mcp_bugbot_gitlab.resources.save_review_state", lambda p, m, s: None)
    result = _aggregate_review_findings_impl({"project_id": "test", "mr_iid": 1})
    findings = result["findings"]
    assert len(findings) == 2
    assert any(f["file"] == "file1.py" for f in findings)
    assert any(f["file"] == "file2.py" for f in findings)

def test_aggregate_review_findings_empty(monkeypatch):
    state = {"chunk_review_progress": {}}
    monkeypatch.setattr("mcp_bugbot_gitlab.resources.get_review_state", lambda p, m: state)
    monkeypatch.setattr("mcp_bugbot_gitlab.resources.save_review_state", lambda p, m, s: None)
    result = _aggregate_review_findings_impl({"project_id": "test", "mr_iid": 1})
    assert result["findings"] == []
    assert "Strengths:\n- None noted." in result["summary"]
    assert "Concerns/Suggestions:\n- None noted." in result["summary"]

def test_aggregate_review_findings_all_duplicates(monkeypatch):
    state = {
        "chunk_review_progress": {
            "file1.py": [
                {"type": "bug", "severity": "high", "file": "file1.py", "line": 10, "message": "Null pointer."},
                {"type": "bug", "severity": "high", "file": "file1.py", "line": 10, "message": "Null pointer."}
            ]
        }
    }
    monkeypatch.setattr("mcp_bugbot_gitlab.resources.get_review_state", lambda p, m: state)
    monkeypatch.setattr("mcp_bugbot_gitlab.resources.save_review_state", lambda p, m, s: None)
    result = _aggregate_review_findings_impl({"project_id": "test", "mr_iid": 1})
    findings = result["findings"]
    assert len(findings) == 1
    assert findings[0]["message"] == "Null pointer."

def test_aggregate_review_findings_different_messages(monkeypatch):
    state = {
        "chunk_review_progress": {
            "file1.py": [
                {"type": "bug", "severity": "high", "file": "file1.py", "line": 10, "message": "Null pointer."},
                {"type": "bug", "severity": "high", "file": "file1.py", "line": 10, "message": "Division by zero."}
            ]
        }
    }
    monkeypatch.setattr("mcp_bugbot_gitlab.resources.get_review_state", lambda p, m: state)
    monkeypatch.setattr("mcp_bugbot_gitlab.resources.save_review_state", lambda p, m, s: None)
    result = _aggregate_review_findings_impl({"project_id": "test", "mr_iid": 1})
    findings = result["findings"]
    assert len(findings) == 2
    messages = [f["message"] for f in findings]
    assert "Null pointer." in messages
    assert "Division by zero." in messages 